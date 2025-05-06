import pybullet as p
from collision.shape.shape import Shape
from collision.shape.shape_registry import register_shape

@register_shape
class Sphere(Shape):
    def __init__(self, radius=0.5):

        super().__init__()
        self.radius = radius
        self.shape_id = p.createCollisionShape(p.GEOM_SPHERE, radius=self.radius)


    def init_shape(self):
        self.body_id = p.createMultiBody(
            baseMass = 1.0,
            baseCollisionShapeIndex = self.shape_id,
            basePosition = [0, 0, 0],
        )

    def get_type(self):
        return "Sphere"
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "radius": self.radius
        }
    
    def get_id(self):
        if not hasattr(self, 'body_id'):
            raise ValueError("Shape has not been initialized. Call init_shape() first.")
        return self.body_id
    
    @classmethod
    def from_dict(data):
        radius = data.get("radius", 0.5)
        return Sphere(radius)
