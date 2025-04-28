import numpy as np
import objects.node as Node

'''
root
name

getRoot()
addNode(node)
moveNode(node)
'''

class SceneGraph:
    def __init__(self, node=None):
        if node:
            self.root = node
        else:
            self.root = Node.Node("root", np.identity(4), None)


    def get_name(self):
        return self.root.get_name()

    def get_root(self):
        return self.root

    def add_node(self, node):
        node.attach(self.root)

    def move_node(self, node, parent_node):
        node.attach(parent_node)