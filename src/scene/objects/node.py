import numpy as np
from core.component_registry import component_registry
from utilities.lock_ordering import ordered_locks
import pyee
from readerwriterlock import rwlock

class Node:
    def __init__(self, name, transform=np.identity(4), parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.components = []
        self.transform = transform
        self.event_emitter = pyee.EventEmitter()
        if parent:
            parent.add_child(self)
        self.lock = rwlock.RWLockFair()


    def attach(self, parent_node):
        with self.lock.gen_wlock():
            if self.parent:
                self.parent.remove_child(self)
            parent_node.add_child(self)
            self.parent = parent_node

    def detach(self):
        with self.lock.gen_wlock():
            if self.parent:
                self.parent.remove_child(self)
                self.parent = None

    def get_name(self):
        with self.lock.gen_rlock():
            return self.name

    def rename(self, new_name):
        with self.lock.gen_wlock():
            self.name = new_name

    def call_event(self, event, *args, **kwargs):
        with self.lock.gen_rlock():
            event_emitter = self.event_emitter
            
        event_emitter.emit(event, *args, **kwargs)

    def call_event_rec(self, event, *args, **kwargs):
        with self.lock.gen_rlock():
            children = list(self.children)
        self.call_event(event, *args, **kwargs)
        for child in self.children:
            child.call_event_rec(event, *args, **kwargs)

    def subscribe_children_rec(self):
        with self.lock.gen_rlock():
            children = list(self.children)
        self.subscribe_components()
        for child in children:
            child.subscribe_children_rec()
        

    def subscribe_components(self):
        with self.lock.gen_rlock():
            components = self.components
            event_emitter = self.event_emitter
        for component in components:
            component.subscribe(event_emitter)




    # Child management

    def add_child(self, child_node):
        with self.lock.gen_wlock():
            self.children.append(child_node)
            child_node.parent = self

    def remove_child(self, child_node):
        with self.lock.gen_wlock():
            if child_node in self.children:
                self.children.remove(child_node)
                child_node.parent = None

    def get_children(self):
        with self.lock.gen_rlock():
            return self.children
    
    def get_parent(self):
        with self.lock.gen_rlock():
            return self.parent


    # Component management

    def add_component(self, component):
        with self.lock.gen_wlock():
            if component in self.components:
                raise ValueError("Component already added to this node.")
            self.components.append(component)
            component.attach(self)

    def remove_component(self, component):
        with self.lock.gen_wlock():
            if component in self.components:
                self.components.remove(component)
            if component.get_parent() != self:
                raise ValueError("Component is not attached to this node.")
            component.unsubscribe_all(self.event_emitter)
            component.parent = None


    def get_components(self):
        with self.lock.gen_rlock():
            return list(self.components)
    
    def get_component(self, name):
        with self.lock.gen_rlock():
            for component in self.components:
                if component.get_name() == name:
                    return component
            return None


    # Transform management

    def get_world_transform(self):
        parent = self.get_parent()
        if parent:
            with ordered_locks([self, parent], lock_type="gen_rlock"):
                local_transform = self.transform
                parent_transform = parent.get_world_transform()
                world_transform = np.dot(parent_transform, local_transform)
        else:
            with self.lock.gen_rlock():
                world_transform = self.transform
        return world_transform

    def get_local_transform(self):
        with self.lock.gen_rlock():
            return self.transform
    
    def set_local_transform(self, transform):
        if transform.shape != (4, 4):
            raise ValueError("Transform must be a 4x4 matrix.")
        with self.lock.gen_wlock():
            self.transform = transform

    def apply_transform(self, transform):
        # If transform is list, convert to 4x4 numpy array
        if isinstance(transform, list):
            transform = np.array(transform).reshape((4, 4))
        if transform.shape != (4, 4):
            raise ValueError("Transform must be a 4x4 matrix.")
        with self.lock.gen_wlock():
            self.transform = np.dot(self.transform, transform)
    # Prefab support

    def to_dict(self):
        with self.lock.gen_rlock():
            return {
                "name": self.name,
                "transform": self.transform.tolist(),  # Convert numpy array to list for JSON serialization
                "children": [child.to_dict() for child in self.children],
                "components": [component.to_dict() for component in self.components]
            }

    @classmethod
    def from_dict(cls, data, scene_manager):
        #print(component_registry)
        name = data.get("name", "Node")
        transform = np.array(data.get("transform", np.identity(4)))
        node = Node(name, transform)
        for child_data in data.get("children", []):
            child_node = Node.from_dict(child_data, scene_manager)
            node.add_child(child_node)
        for component_data in data.get("components", []):
            #print(component_data)
            component_type = component_data.get("type")
            if component_type in component_registry:
                component = component_registry[component_type].from_dict(component_data, scene_manager)
                node.add_component(component)
            else:
                raise ValueError(f"Unknown component type: {component_type}")
        return node 