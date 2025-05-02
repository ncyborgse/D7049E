
from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def subscribe(self, event_emitter):
        # Subscribe a number of functions to the event emitter
        pass

    @abstractmethod
    def on_runtime_init(self, scene_manager):
        # Called when the runtime is initialized
        pass

    def attach(self, node):
        node.add_component(self)

    def get_name(self):
        return self.name
    
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.__class__.__name__
            # Subclass-specific attributes can be added here
        }


    @classmethod
    @abstractmethod
    def from_dict(self, data):
        # Populate the component from a dictionary
        pass