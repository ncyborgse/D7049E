import numpy as np
from scene.objects.node import Node
import threading

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
        self.lock = threading.Lock()

    def get_root(self):
        with self.lock:
            return self.root

    def add_node(self, node):
        with self.lock:
            node.attach(self.root)

    def move_node(self, node, parent_node):
        with self.lock:
            node.attach(parent_node)

    # Recursive function to find a node by name in the scene graph
    def get_by_name_in(self, root, name):
        with self.lock:
            if root.get_name() == name:
                return root
            for child in root.get_children():
                result = self.get_by_name_in(child, name)
                if result:
                    return result
            return None

    def get_name(self):
        with self.lock:
            return self.name
    
    def rename(self, name):
        with self.lock:
            self.name = name
