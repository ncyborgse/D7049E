from core.component_registry import register_component
from collision.shape.shape_registry import shape_registry
from scene.component.component import Component
from collision.collision_manager import CollisionManager
from collision.shape.shape import Shape
import numpy as np
import threading
from readerwriterlock import rwlock 

@register_component
class Collider(Component):
    def __init__(self, name="Collider"):
        super().__init__(name=name)
        self.shape = None
        self.transform = None
        self.enabled = True
        self.lock = rwlock.RWLockFair()

    def register_collision_manager(self, collision_manager):
        with self.lock.gen_wlock():
            self.collision_manager = collision_manager

    def subscribe(self, event_emitter):
        with self.lock.gen_wlock():
            # On spawn, add the collider to the collision manager
            event_emitter.on("onSpawn", self.add_collider)
            # On destroy, remove the collider from the collision manager
            event_emitter.on("onDestroy", self.remove_collider)
        

    def add_collider(self):
        with self.lock.gen_wlock():
            # Check if the collider is enabled before adding it to the collision manager
            if self.enabled and self.collision_manager:
                self.collision_manager.add_collider(self)
            
            
    def remove_collider(self):
        with self.lock.gen_wlock():
            if self.enabled and self.collision_manager:
                self.collision_manager.remove_collider(self)    

    def enable(self):
        with self.lock.gen_wlock():
            if self.enabled:
                raise RuntimeError("Collider is already enabled.")
            self.enabled = True
            self.add_collider()

    def disable(self):
        with self.lock.gen_wlock():
            if not self.enabled:
                raise RuntimeError("Collider is already disabled.")
            self.enabled = False
            self.remove_collider()

    def set_shape(self, shape):
        if not isinstance(shape, Shape):
            raise TypeError("Shape must be an instance of Shape or its subclasses.")
        with self.lock.gen_wlock():
            # Ensure shape is a subclass of Shape

            self.shape = shape

    def get_shape(self):
        with self.lock.gen_rlock():
            return self.shape
    
    def set_transform(self, transform):
        if transform.shape != (4, 4):
            raise ValueError("Transform must be a 4x4 matrix.")
        
        with self.lock.gen_wlock():
            # Ensure transform is a 4x4 matrix
            self.transform = transform


    def get_transform(self):
        with self.lock.gen_rlock():
            transform = self.transform
            if transform is None or transform.__str__() == "None": # idk why this is needed but it is
                return np.identity(4)
            return self.transform
    
    def get_world_transform(self):
        parent = self.get_parent()
        node_transform = parent.get_world_transform() if parent else np.identity(4)
        collider_transform = self.get_transform()
        with self.lock.gen_rlock():
            return np.dot(node_transform, collider_transform)
    
    def to_dict(self):
        with self.lock.gen_rlock():
            base = super().to_dict()
            base.update({
                "shape": self.shape.to_dict() if self.shape else None,
                "transform": self.transform.tolist() if self.transform is not None else None,
                "enabled": self.enabled
            })
            return base
    
    @classmethod
    def from_dict(cls, data, scene_manager):
        shape_data = data.get("shape")
        collider = Collider(name=data.get("name", "Collider"))
        collider.enabled = data.get("enabled", True)
        collider.transform = np.array(data.get("transform", np.identity(4)))
        shape_type = shape_data.get("type")
        if shape_type in shape_registry:
            shape = shape_registry[shape_type].from_dict(shape_data, scene_manager)
            collider.set_shape(shape)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
        return collider
    



    
