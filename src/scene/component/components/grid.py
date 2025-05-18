from readerwriterlock import rwlock
from scene.component.component import Component
from core.component_registry import register_component


@register_component
class Grid(Component):
    def __init__(self, name="Grid"):
        super().__init__(name=name)
        self.lock = rwlock.RWLockFair()

    def subscribe(self, event_emitter):
        pass

    def to_dict(self):
        base = super().to_dict()
        return base

    def from_dict(cls, data, scene_manager):
        name = data.get("name", "Grid")
        grid = cls(name=name)
        return grid

                

    






    
