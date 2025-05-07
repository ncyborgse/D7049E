
from abc import ABC, abstractmethod
import threading

class Component(ABC):
    def __init__(self, name):
        self.name = name
        self.subscriptions = []
        self.parent = None
        self.lock = threading.RLock()

    @abstractmethod
    def subscribe(self, event_emitter):
        # Subscribe a number of functions to the event emitter
        pass

    def subscribe_to(self, event_emitter, event, callback):
        with self.lock:
            # Subscribe a single function to the event emitter
            if callable(callback):
                self.subscriptions.append((event, callback))
                event_emitter.on(event, callback)
            else:
                raise TypeError(f"Callback for event '{event}' is not callable.")
        
    def unsubscribe_all(self, event_emitter):
        with self.lock:
            # Unsubscribe a number of functions from the event emitter
            for subscription in self.subscriptions:
                event_emitter.remove_listener(subscription[0], subscription[1])
            self.subscriptions = []

    def attach(self, node):
        with self.lock:
            self.parent = node

    def get_name(self):
        return self.name
    
    def to_dict(self):
        with self.lock:
            return {
                "name": self.name,
                "type": self.__class__.__name__
                # Subclass-specific attributes can be added here
            }
    
    def get_parent(self):
        return self.parent

    @classmethod
    @abstractmethod
    def from_dict(self, data, scene_manager):
        # Populate the component from a dictionary
        pass