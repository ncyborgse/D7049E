import threading


class SceneManager:
    def __init__(self):
        self.scenes = []
        self.current_scene_index = None
        self.current_cameras = []
        self.lock = threading.RLock()

    def add_scene(self, scene):
        with self.lock:
            if scene not in self.scenes:
                self.scenes.append(scene)
                if self.current_scene_index is None:
                    self.current_scene_index = 0

    def get_scenes(self):
        with self.lock:
            return self.scenes

    def get_current_scene(self):
        with self.lock:
            if self.current_scene_index is not None:
                return self.scenes[self.current_scene_index]
            return None

    def get_current_cameras(self):
        with self.lock:
            return self.current_camera
        
    def set_current_scene(self, scene):
        with self.lock:
            if scene in self.scenes:
                self.current_scene_index = self.scenes.index(scene)
            else:
                raise ValueError("Scene not found in scene list.")

    def remove_scene(self, index):
        with self.lock:
            if 0 <= index < len(self.scenes):
                del self.scenes[index]
                if self.current_scene_index == index:
                    self.current_scene_index = None if not self.scenes else 0
            else:
                raise IndexError("Scene index out of range.")

    def load_scene(self, scene_name):
        with self.lock:
            for index, scene in enumerate(self.scenes):
                print(scene.get_name())
                if scene.get_name() == scene_name:
                    self.current_scene_index = index


                    # Look for the current camera in the scene

                    root = scene.get_root()
                    nodes_to_check = [root]
                    list_of_cameras = []

                    while nodes_to_check:
                        current_node = nodes_to_check.pop()
                        camera = current_node.get_component("Camera")
                        if camera:
                            list_of_cameras.append(camera)

                        # Add children to the list for further checking
                        for child in current_node.get_children():
                            nodes_to_check.append(child)

                        self.current_cameras = list_of_cameras

                    return scene
            raise ValueError(f"Scene '{scene_name}' not found.")
