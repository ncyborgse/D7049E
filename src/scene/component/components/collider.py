from core.component_registry import register_component
from scene.component.component import Component
import pybullet as p

@register_component
class Collider(Component):
    def __init__(self, collision_manager, name="Collider"):
        super().__init__(name=name)
        self.collision_manager = collision_manager
        self.shape = None
        self.transform = None
        self.enabled = True


    def subscribe(self, event_emitter):
        # On spawn, add the collider to the collision manager
        event_emitter.on("onSpawn", self.add_collider)
        # On destroy, remove the collider from the collision manager
        event_emitter.on("onDestroy", self.remove_collider)
        

    def add_collider(self):
        if self.enabled:
            self.collision_manager.add_collider(self)

    def remove_collider(self):
        if self.enabled:
            self.collision_manager.remove_collider(self)    

    def enable(self):
        if self.enabled:
            raise RuntimeError("Collider is already enabled.")
        self.enabled = True
        self.collision_manager.add_collider(self)

    def disable(self):
        if not self.enabled:
            raise RuntimeError("Collider is already disabled.")
        self.enabled = False
        self.collision_manager.remove_collider(self)

    def set_shape(self, shape):
        #IMPLENT!!!!
        pass


    def get_shape(self):
        return self.shape
    
    def set_transform(self, transform):
        # Ensure transform is a 4x4 matrix
        if transform.shape != (4, 4):
            raise ValueError("Transform must be a 4x4 matrix.")
        self.transform = transform


    def get_transform(self):
        return self.transform
    
    



    
