import threading
import numpy as np
from scene.component.component import Component
from core.component_registry import register_component


@register_component
class Camera(Component):
    def __init__(self, name="Camera"):
        super().__init__(name=name)

        self.eye = [0.0, 0.0, 0.0]
        self.target = [0.0, 0.0, -1.0]
        self.up = [0.0, 1.0, 0.0]

        self.lock = threading.RLock()


    def get_eye(self):
        with self.lock:
            return self.eye

    def get_target(self):
        with self.lock:
            return self.target

    def get_up(self):
        with self.lock:
            return self.up


    def set_eye(self, eye):
        if not isinstance(eye, list) or len(eye) != 3:
            raise ValueError("Eye position must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in eye):
            raise ValueError("Eye position must contain only numbers.")

        with self.lock:
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

        with self.lock:
            target = np.array(target + [1.0])
            if self.get_parent():
                world_target = self.get_parent().transform @ target
                self.target = world_target[:3]
            else:
                self.target = target[:3]

    def set_up(self, up):
        if not isinstance(up, list) or len(up) != 3:
            raise ValueError("Up vector must be a list of three floats.")
        if not all(isinstance(i, (int, float)) for i in up):
            raise ValueError("Up vector must contain only numbers.")

        with self.lock:
            up = np.array(up + [0.0])
            if self.get_parent():
                world_up = self.get_parent().transform @ up
                self.up = world_up[:3]
            else:
                self.up = up[:3]


    def subscribe(self, event_emitter):
        with self.lock:
            supported_events = ['onStart', 'onUpdate', 'onRender', 'onSpawn', 'onDestroy', 'overlap', 'enter', 'exit']

    def to_dict(self):
        with self.lock:
            base = super().to_dict()
            # Update base
            return base

    @classmethod
    def from_dict(cls, data, scene_manager):
        pass
