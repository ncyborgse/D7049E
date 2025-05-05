import time

class Engine:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.is_running = False


    def run(self):
        self.is_running = True
        previous_time = time.time()

        # Subscribe all components to their nodes event emitters

        scene_graph = self.scene_manager.get_current_scene()
        root = scene_graph.get_root()
        if root:
            root.subscribe_children_rec()
        else:
            raise RuntimeError("Root node not found in the scene graph.")

        while self.is_running:
            # Update each frame with delta time
            current_time = time.time()
            delta_time = current_time - previous_time

            previous_time = current_time

            scene_graph = self.scene_manager.get_current_scene()

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
            time.sleep(0.016)


    def stop(self):
        self.is_running = False