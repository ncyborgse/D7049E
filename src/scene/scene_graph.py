import numpy as np
from scene.objects.node import Node

'''
root
name

getRoot()
addNode(node)
moveNode(node)
'''

class SceneGraph:
    def __init__(self, node=None, name="Scene"):
        self.name = name
        if node:
            self.root = node
        else:
            self.root = Node("root", np.identity(4), None)

    def get_root(self):
        return self.root

    def add_node(self, node):
        node.attach(self.root)

    def move_node(self, node, parent_node):
        node.attach(parent_node)

    # Recursive function to find a node by name in the scene graph
    def get_by_name_in(self, root, name):
        if root.get_name() == name:
            return root
        for child in root.get_children():
            result = self.get_by_name_in(child, name)
            if result:
                return result
        return None

    def get_name(self):
        return self.name
    
    def rename(self, name):
        self.name = name
    


