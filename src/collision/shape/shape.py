from abc import ABC, abstractmethod


class Shape(ABC):

    @abstractmethod
    def get_type(self):
        """Return the type of the shape."""
        pass

    @abstractmethod
    def to_dict(self):
        """Convert the shape to a dictionary."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(data):
        """Create a shape from a dictionary."""
        pass
    
    @abstractmethod
    def get_id(self):
        pass
    
