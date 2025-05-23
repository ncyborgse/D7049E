import pybullet as p
from scipy.spatial.transform import Rotation as R
import time
import numpy as np

from readerwriterlock import rwlock


class CollisionManager:
    def __init__(self, scene_manager, shutdown_event, frame_rate=60):
        self.colliders = []
        self.scene_manager = scene_manager
        self.prev_collisions = []
        self.physics_client = p.connect(p.DIRECT)  # Connect to PyBullet in DIRECT mode
        p.setGravity(0, 0, 0)  # Set gravity for the simulation
        self.is_running = False
        self.frame_rate = frame_rate  # Set the desired frame rate
        p.setTimeStep(1.0 / self.frame_rate)  # Set the time step for the simulation
        self.shutdown_event = shutdown_event
        self.click_queue = []  # Queue for click events
        self.lock = rwlock.RWLockFair()  # Lock for thread-safe access



    def register_colliders(self):
        for scene in self.scene_manager.get_scenes():
            root = scene.get_root()
            nodes_to_check = [root]

            while nodes_to_check:
                current_node = nodes_to_check.pop()
                collider = current_node.get_component("Collider")
                if collider:
                    collider.register_collision_manager(self)
                    collider.get_shape().init_shape()  # Initialize the shape
                    self.colliders.append(collider)

                # Add children to the list for further checking
                for child in current_node.get_children():
                    nodes_to_check.append(child)

    def queue_click_event(self, ray_from, ray_to):

        with self.lock.gen_wlock():
            self.click_queue.append((ray_from, ray_to))


    def check_collisions(self, delta_time=None):        

        collision_map = {}
        p.stepSimulation(physicsClientId=self.physics_client, )  # Step the simulation to update positions

    

        for collider in self.colliders:
            shape = collider.get_shape()
            id = shape.get_id()

            if id not in collision_map:
                collision_map[id] = {
                    "collider": collider,
                    "new": [],
                    "ongoing": [],
                    "ending": []
                }

            transform = collider.get_world_transform()

            rotation_matrix = transform[:3, :3]
            quaternion = R.from_matrix(rotation_matrix).as_quat()
            p.resetBasePositionAndOrientation(id, transform[:3, 3], quaternion)

        ids = list(collision_map.keys())

        # Perform collision detection
        collision_pairs = p.getContactPoints()
        
        # Separate collisions into new, ongoing, and ending collisions

        collision_pairs = set(
            tuple(sorted((cp[1], cp[2]))) for cp in collision_pairs if cp[1] != cp[2]
        )

        for pair in collision_pairs:


            if pair not in self.prev_collisions:
                collision_map[pair[0]]["new"].append(collision_map[pair[1]]["collider"].get_parent())
                collision_map[pair[1]]["new"].append(collision_map[pair[0]]["collider"].get_parent())

            collision_map[pair[0]]["ongoing"].append(collision_map[pair[1]]["collider"].get_parent())
            collision_map[pair[1]]["ongoing"].append(collision_map[pair[0]]["collider"].get_parent())

        for pair in self.prev_collisions:
            if pair not in collision_pairs:
                collision_map[pair[0]]["ending"].append(collision_map[pair[1]]["collider"].get_parent())
                collision_map[pair[1]]["ending"].append(collision_map[pair[0]]["collider"].get_parent())

        # Update the previous collisions list
        self.prev_collisions = collision_pairs

        # Send events to colliders
        for shape_id, collision_data in collision_map.items():
            collider = collision_data["collider"]
            node = collider.get_parent()
            if collision_data["new"]:
                node.call_event("enter", collision_data["new"])
            if collision_data["ongoing"]:
                node.call_event("overlap", collision_data["ongoing"])
            if collision_data["ending"]:
                node.call_event("exit", collision_data["ending"])

        # Process click events from the queue
        with self.lock.gen_rlock():
            click_events = self.click_queue.copy()
        
        for event in click_events:
            ray_from, ray_to = event
           

            hits = p.rayTest(ray_from, ray_to, physicsClientId=self.physics_client)

            for hit in hits:
                # Check if ray hit a registered collider
                if hit[0] in ids:
                    collider = collision_map[hit[0]]["collider"]
                    node = collider.get_parent()
                    
                    # Check if node has clickable component

                    clickable = node.get_component("Clickable")
                    if clickable:
                        if clickable.is_enabled():
                            clickable.click()
                            break  # Break after the first clickable hit

        with self.lock.gen_wlock():
            self.click_queue.clear()

    def run(self):
        print("CollisionManager is running.")
        # Main loop for the collision manager


        while not self.shutdown_event.is_set():

            self.check_collisions()

            # Sleep for a short duration to limit the frame rate
            time.sleep(1.0 / self.frame_rate)



                

                




