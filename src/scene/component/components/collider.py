from core.component_registry import register_component
from scene.component.component import Component

@register_component
class Collider(Component):
    def __init__(self, collision_manager, name="Collider"):
        super().__init__(name=name)
        self.collision_manager = collision_manager
        self.shape = None
        self.transform = None
        self.enabled = True


    
