import time

class Engine:
    def __init__(self, scene_manager, shutdown_event, frame_rate=60):
        self.frame_rate = frame_rate
        self.scene_manager = scene_manager
        self.shutdown_event = shutdown_event


    def run(self):
        print("Starting engine")
        previous_time = time.time()

        # Subscribe all components to their nodes event emitters

        print("Subscribing all components to their nodes event emitters")
        scene_graph = self.scene_manager.get_current_scene()
        root = scene_graph.get_root()
        print("Root node found")
        if root:
            root.subscribe_children_rec()
        else:
            raise RuntimeError("Root node not found in the scene graph.")

        print("Starting engine loop")
        while not self.shutdown_event.is_set():
            # Update each frame with delta time
            current_time = time.time()
            delta_time = current_time - previous_time

            previous_time = current_time

            print("getting current scene")
            scene_graph = self.scene_manager.get_current_scene()
            print("Current scene retrieved")

            # Call the update method on all nodes in the scene graph

            if scene_graph:
                root_node = scene_graph.get_root()
                if root_node:
                    root_node.call_event_rec("onUpdate", delta_time)

                else:
                    raise RuntimeError("Root node not found in the scene graph.")
            else:
                raise RuntimeError("No scene graph loaded.")
            
            # Sleep for a short duration to limit the frame rate
            time.sleep(1.0 / self.frame_rate)
