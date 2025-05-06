import numpy as np
from core.component_registry import component_registry
import pyee

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


    def attach(self, parent_node):
        if self.parent:
            self.parent.remove_child(self)
        parent_node.add_child(self)
        self.parent = parent_node

    def get_name(self):
        return self.name

    def get_event_emitter(self):
        return self.event_emitter

    def call_event(self, event, *args, **kwargs):
        self.event_emitter.emit(event, *args, **kwargs)

    def call_event_rec(self, event, *args, **kwargs):
        self.call_event(event, *args, **kwargs)
        for child in self.children:
            child.call_event_rec(event, *args, **kwargs)

    def subscribe_children_rec(self):
        for component in self.components:
            component.subscribe(self.event_emitter)
        for child in self.children:
            child.subscribe_children_rec()

    def rename(self, new_name):
        self.name = new_name


    # Child management

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def remove_child(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)
            child_node.parent = None

    def get_children(self):
        return self.children


    # Component management

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)

    def get_components(self):
        return self.components
    
    def get_component(self, name):
        for component in self.components:
            if component.get_name() == name:
                return component
        return None


    # Transform management

    def get_world_transform(self):
        if self.parent:
            return np.dot(self.parent.get_world_transform(), self.transform)
        else:
            return self.transform

    def get_local_transform(self):
        return self.transform
    
    # Prefab support

    def to_dict(self):
        return {
            "name": self.name,
            "transform": self.transform.tolist(),  # Convert numpy array to list for JSON serialization
            "children": [child.to_dict() for child in self.children],
            "components": [component.to_dict() for component in self.components]
        }

    @classmethod
    def from_dict(data, scene_manager):
        name = data.get("name", "Node")
        transform = np.array(data.get("transform", np.identity(4)))
        node = Node(name, transform)
        for child_data in data.get("children", []):
            child_node = Node.from_dict(child_data, scene_manager)
            node.add_child(child_node)
        for component_data in data.get("components", []):
            component_type = component_data.get("type")
            if component_type in component_registry:
                component = component_registry[component_type].from_dict(component_data, scene_manager)
                node.add_component(component)
            else:
                raise ValueError(f"Unknown component type: {component_type}")
        return node