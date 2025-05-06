import pybullet as p
from scipy.spatial.transform import Rotation as R


class CollisionManager:
    def __init__(self, scene_manager):
        self.colliders = []
        self.scene_manager = scene_manager
        self.prev_collisions = []
        self.physics_client = p.connect(p.DIRECT)  # Connect to PyBullet in DIRECT mode
        p.setGravity(0, 0, 0)  # Set gravity for the simulation



    def register_colliders(self):
        for scene in self.scene_manager.get_scenes():
            root = scene.get_root()
            nodes_to_check = [root]

            while nodes_to_check:
                current_node = nodes_to_check.pop()
                collider = current_node.get_component("Collider")
                if collider:
                    collider.register_collision_manager(self)
                    self.colliders.append(collider)

                # Add children to the list for further checking
                for child in current_node.get_children():
                    nodes_to_check.append(child)

    def check_collisions(self):
        # Move all pybullet shapes to their correct positions
        collision_map = {}

    

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



        pos1 = p.getBasePositionAndOrientation(ids[0])[0]
        pos2 = p.getBasePositionAndOrientation(ids[1])[0]
        print("Position 1:", pos1)
        print("Position 2:", pos2)
        shape1 = p.getVisualShapeData(ids[0])
        shape2 = p.getVisualShapeData(ids[1])
        print("Shape 1:", shape1)
        print("Shape 2:", shape2)
        contact_points = p.getContactPoints(bodyA=ids[0], bodyB=ids[1])
        print("Contact points:", contact_points)

        # Perform collision detection
        collision_pairs = p.getContactPoints()

        print("Collision pairs:", collision_pairs)


        
        # Separate collisions into new, ongoing, and ending collisions

        collision_pairs = set(
            tuple(sorted((cp[1], cp[2]))) for cp in collision_pairs if cp[1] != cp[2]
        )

        for pair in collision_pairs:

            # Sort collision pairs to guarantee consistent ordering

            pair[0], pair[1] = sorted(pair[:2])
            if pair not in self.prev_collisions:
                collision_map[pair[0]]["new"].append(pair[1])
                collision_map[pair[1]]["new"].append(pair[0])

            collision_map[pair[0]]["ongoing"].append(pair[1])
            collision_map[pair[1]]["ongoing"].append(pair[0])

        for pair in self.prev_collisions:
            if pair not in collision_pairs:
                collision_map[pair[0]]["ending"].append(pair[1])
                collision_map[pair[1]]["ending"].append(pair[0])

        # Update the previous collisions list
        self.prev_collisions = collision_pairs

        # Send events to colliders
        for shape_id, collision_data in collision_map.items():
            collider = collision_data["collider"]
            node = collider.get_parent()
            node.call_event("enter", collision_data["new"])
            node.call_event("overlap", collision_data["ongoing"])
            node.call_event("exit", collision_data["ending"])



                

                




