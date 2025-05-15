from scene.component.component import Component
from core.component_registry import register_component
from readerwriterlock import rwlock

@register_component
class Clickable(Component):
    def __init__(self, name="Clickable"):
        super().__init__(name=name)
        self.enabled = True
        self.lock = rwlock.RWLockFair()

    def subscribe(self, event_emitter):
        with self.lock.gen_wlock():
            # Subscribe to events related to clickables
            event_emitter.on("onStart", self.check_for_collider)

    def click(self):
        parent = self.get_parent()
        if parent:
            parent.call_event("onClick", self)
        else:
            raise RuntimeError("Parent node not found. Cannot emit click event.")

    def enable(self):
        with self.lock.gen_wlock():
            if self.enabled:
                raise RuntimeError("Clickable is already enabled.")
            self.enabled = True
    
    def disable(self):
        with self.lock.gen_wlock():
            if not self.enabled:
                raise RuntimeError("Clickable is already disabled.")
            self.enabled = False

    def is_enabled(self):
        with self.lock.gen_rlock():
            return self.enabled

    def check_for_collider(self):
        parent = self.get_parent()
        collider = parent.get_component("Collider")
        if not collider:
            raise RuntimeError("Clickable component requires a Collider component on the parent node.")
        if not collider.is_enabled():
            raise RuntimeError("Collider component is not enabled. Clickable cannot function without an enabled Collider.")

    def to_dict(self):
        base = super().to_dict()
        base["enabled"] = self.enabled
        return base


    @classmethod
    def from_dict(cls, data, scene_manager):
        name = data.get("name", "Clickable")
        enabled = data.get("enabled", True)
        clickable = cls(name=name)
        clickable.enabled = enabled
        return clickable