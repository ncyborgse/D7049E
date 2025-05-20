import threading
import numpy as np
from scene.component.component import Component
from core.component_registry import register_component
from readerwriterlock import rwlock


@register_component
class Camera(Component):
    def __init__(self, name="Camera"):
        super().__init__(name=name)

        self.eye = np.array([0.0, 0.0, 0.0])
        self.target = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])

        self.lock = rwlock.RWLockFair()


    def get_eye(self):
        if self.get_parent():
            parent = self.get_parent()
        with self.lock.gen_rlock():
            eye = np.array(self.eye.tolist() + [1.0])
            if parent:
                world_eye = parent.transform @ eye
                eye = np.array(world_eye[:3])
            else:
                eye = np.array(eye[:3])
        return eye
        


    def get_target(self):
        if self.get_parent():
            parent = self.get_parent()
        with self.lock.gen_rlock():
            target = np.array(self.target.tolist() + [1.0])
            if parent:
                world_target = parent.transform @ target
                target = np.array(world_target[:3])
            else:
                target = np.array(target[:3])
        return target

    def get_up(self):
        if self.get_parent():
            parent = self.get_parent()
        with self.lock.gen_rlock():
            up = np.array(self.up.tolist() + [0.0])
            if parent:
                world_up = parent.transform @ up
                up = np.array(world_up[:3])
            else:
                up = np.array(up[:3])
        return up


    def set_eye(self, eye):
        if not isinstance(eye, list) or len(eye) != 3:
            raise ValueError("Eye position must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in eye):
            raise ValueError("Eye position must contain only numbers.")

        with self.lock.gen_wlock():
            self.eye = np.array(eye)

    def set_target(self, target):
        if not isinstance(target, list) or len(target) != 3:
            raise ValueError("Target position must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in target):
            raise ValueError("Target position must contain only numbers.")
        
        with self.lock.gen_wlock():
            self.target = np.array(target)

    def set_up(self, up):
        if not isinstance(up, list) or len(up) != 3:
            raise ValueError("Up vector must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in up):
            raise ValueError("Up vector must contain only numbers.")
        with self.lock.gen_wlock():
            self.up = np.array(up)



    def subscribe(self, event_emitter):
        pass

    def to_dict(self):
        with self.lock.gen_rlock():
            base = super().to_dict()
            base.update({
                "eye": self.eye.tolist(),
                "target": self.target.tolist(),
                "up": self.up.tolist()
            })
            print("Transforming camera " + self.name + " to dict")
            return base

    @classmethod
    def from_dict(cls, data, scene_manager):
        camera = Camera(name=data.get("name", "Camera"))
        camera.eye = np.array(data.get("eye", [0.0, 0.0, 0.0]))
        camera.target = np.array(data.get("target", [0.0, 0.0, -1.0]))
        camera.up = np.array(data.get("up", [0.0, 1.0, 0.0]))
        return camera
