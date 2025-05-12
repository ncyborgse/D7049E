import threading
import numpy as np
from scene.component.component import Component
from core.component_registry import register_component
from readerwriterlock import rwlock


@register_component
class Camera(Component):
    def __init__(self, name="Camera"):
        super().__init__(name=name)

        self.eye = [0.0, 0.0, 0.0]
        self.target = [0.0, 0.0, -1.0]
        self.up = [0.0, 1.0, 0.0]

        self.lock = rwlock.RWLockFair()


    def get_eye(self):
        with self.lock.gen_rlock():
            return self.eye

    def get_target(self):
        with self.lock.gen_rlock():
            return self.target

    def get_up(self):
        with self.lock.gen_rlock():
            return self.up


    def set_eye(self, eye):
        if not isinstance(eye, list) or len(eye) != 3:
            raise ValueError("Eye position must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in eye):
            raise ValueError("Eye position must contain only numbers.")

        with self.lock.gen_wlock():
            eye = np.array(eye + [1.0])
            if self.get_parent():
                world_eye = self.get_parent().transform @ eye
                self.eye = world_eye[:3]
            else:
                self.eye = eye[:3]

    def set_target(self, target):
        if not isinstance(target, list) or len(target) != 3:
            raise ValueError("Target position must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in target):
            raise ValueError("Target position must contain only numbers.")


        parent = self.get_parent()
        with self.lock.gen_wlock():
            target = np.array(target + [1.0])
            if parent:
                world_target = parent.transform @ target
                self.target = world_target[:3]
            else:
                self.target = target[:3]

    def set_up(self, up):
        if not isinstance(up, list) or len(up) != 3:
            raise ValueError("Up vector must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in up):
            raise ValueError("Up vector must contain only numbers.")


        if self.get_parent():
            parent = self.get_parent()
        with self.lock.gen_wlock():
            up = np.array(up + [0.0])
            if parent:
                world_up = parent.transform @ up
                self.up = world_up[:3]
            else:
                self.up = up[:3]


    def subscribe(self, event_emitter):
        pass

    def to_dict(self):
        with self.lock.gen_rlock():
            base = super().to_dict()
            # Update base
            return base

    @classmethod
    def from_dict(cls, data, scene_manager):
        pass
