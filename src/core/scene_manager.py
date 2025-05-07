import threading


class SceneManager:
    def __init__(self):
        self.scenes = []
        self.current_scene_index = None
        self.lock = threading.Lock()

    def add_scene(self, scene):
        with self.lock:
            if scene not in self.scenes:
                self.scenes.append(scene)
                if self.current_scene_index is None:
                    self.current_scene_index = 0
    
    def get_current_scene(self):
        with self.lock:
            if self.current_scene_index is not None:
                return self.scenes[self.current_scene_index]
            return None

    
    def get_scenes(self):
        with self.lock:
            if self.current_scene_index is not None:
                return self.scenes[self.current_scene_index]
            
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
                    return scene
            raise ValueError(f"Scene '{scene_name}' not found.")