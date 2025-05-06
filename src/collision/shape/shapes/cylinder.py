import pybullet as p
from collision.shape.shape import Shape
from collision.shape.shape_registry import register_shape


@register_shape
class Cylinder(Shape):
    def __init__(self, height=1.0, radius=0.5):

        super().__init__()
        self.height = height
        self.radius = radius

    def init_shape(self):
        self.shape_id = p.createCollisionShape(p.GEOM_CYLINDER, radius=self.radius, height=self.height)
        self.body_id = p.createMultiBody(
            baseMass = 1.0,
            baseCollisionShapeIndex = self.shape_id,
            basePosition = [0, 0, 0],
        )

    def get_type(self):
        return "Cylineder"
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "height": self.height,
            "radius": self.radius
        }
    
    def get_id(self):
        if not hasattr(self, 'body_id'):
            raise ValueError("Shape has not been initialized. Call init_shape() first.")
        return self.body_id
    
    @classmethod
    def from_dict(data):
        height = data.get("height", 1.0)
        radius = data.get("radius", 0.5)
        return Cylinder(height, radius)
