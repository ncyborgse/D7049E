import pybullet as p
from collision.shape.shape import Shape
from collision.shape.shape_registry import register_shape

@register_shape
class Box(Shape):
    def __init__(self, width=1.0, height=1.0, depth=1.0):

        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth

    def init_shape(self):
        half_extents = [self.width / 2, self.height / 2, self.depth / 2]
        self.shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)
        self.body_id = p.createMultiBody(
            baseMass = 1.0,
            baseCollisionShapeIndex = self.shape_id,
            basePosition = [0, 0, 0],
        )

    def get_type(self):
        return "Box"
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "width": self.width,
            "height": self.height,
            "depth": self.depth
        }
    
    def get_id(self):
        if not hasattr(self, 'body_id'):
            raise ValueError("Shape has not been initialized. Call init_shape() first.")
        return self.body_id

    
    @classmethod
    def from_dict(data):
        width = data.get("width", 1.0)
        height = data.get("height", 1.0)
        depth = data.get("depth", 1.0)
        return Box(width, height, depth)
