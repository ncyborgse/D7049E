import threading

## FIX LOCKING PROPERLY

class SceneManager:
    def __init__(self):
        self.scenes = []
        self.current_scene_index = None
        self.current_cameras = []
        self.lock = threading.RLock()

    def add_scene(self, scene):
        print("debug | scene manager/add scene\n")
        with self.lock:
            if scene not in self.scenes:
                self.scenes.append(scene)
                self.set_current_scene(scene)
                if self.current_scene_index is None:
                    self.current_scene_index = 0
        print("debug | SceneManager's scenes in add scene: ", self.scenes, "\n")
        print("debug | SceneManager current_scene_index: ", self.current_scene_index, "\n")

    def get_scenes(self):
        print("debug | SceneManager / get scenes unlocked: ", self.scenes, "\n")
        with self.lock:
            print("debug | SceneManager get scenes LOCK: ", self.scenes, "\n")
            return self.scenes

    def get_current_scene(self):
        #print("debug | scene manager/get current scene: \n", self.scenes[self.current_scene_index])
        with self.lock:
            if self.current_scene_index is not None:
                return self.scenes[self.current_scene_index]
            return None

    def get_current_cameras(self):
        with self.lock:
            return self.current_cameras

    def set_current_scene(self, scene):
        with self.lock:
            if scene in self.scenes:
                self.current_scene_index = self.scenes.index(scene)
            else:
                raise ValueError("Scene not found in scene list.")

    def remove_scene(self, index):
        print("debug | REMOVING A SCENE")
        with self.lock:
            if 0 <= index < len(self.scenes):
                del self.scenes[index]
                if self.current_scene_index == index:
                    self.current_scene_index = None if not self.scenes else 0
            else:
                raise IndexError("Scene index out of range.")

    def load_scene(self, scene_name):
        print("debug | (in load_scene) before the LOCK")
        with self.lock:
            for index, scene in enumerate(self.scenes):
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

                    print("debug | (scene manager / load_scene) self.current_scene_index: ", self.current_scene_index, "\n")
                    print("debug | (scene manager / load_scene) return scene: ", scene, "\n")

                    return scene
            raise ValueError(f"Scene '{scene_name}' not found.")
