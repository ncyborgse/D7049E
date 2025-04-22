'''
root

invoke()?
getRoot()
'''

class SceneGraph:
    def __init__(self, node=None):
        if node:
            self.root = node
        else:
            self.root = Node("root", None)
        self.nodes = [self.root]

    def add_node(self, node):
        self.nodes.append(node)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def get_root(self):
        return self.root

    def invoke(self, event):
        pass