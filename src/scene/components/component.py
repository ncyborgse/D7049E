
from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def subscribe(self, event_emitter):
        # Subscribe a number of functions to the event emitter
        pass

    def attach(self, node):
        node.add_component(self)

    def get_name(self):
        return self.name