'''
name/id
transform
parent
children
components

attach(parent)
add/removeComponent(component)
getComponents/Children()
getWoldtransform()
getLocaltransform()
callEvent(Event)
'''

class Node:
    def __init__(self, name, transform, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.components = []
        if parent:
            parent.add_child(self)
            self.transform = parent.getTransform() * transform


    def attach(self, parent_node):
        if self.parent:
            self.parent.remove_child(self)
        parent_node.add_child(self)

    def get_name(self):
        return self.name

    def call_event(self, event):
        pass


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


    # Transform management

    def get_world_transform(self):
        if self.parent:
            return self.parent.get_world_transform() * self.transform
        else:
            return self.transform
    
    def get_local_transform(self):
        return self.transform