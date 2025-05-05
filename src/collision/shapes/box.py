import pybullet as p
from collision.shapes.shape import Shape


class Box(Shape):
    def __init__(self, width=1.0, height=1.0, depth=1.0):

        super().__init__()
        self.width = width
        self.height = height
        self.depth = depth

    def get_type(self):
        return "Box"
    
    def to_dict(self):
        return {
            "type": self.get_type(),
            "width": self.width,
            "height": self.height,
            "depth": self.depth
        }
    
    def create_shape(self):
        # Create a box shape in PyBullet
        half_extents = [self.width / 2, self.height / 2, 0.1]
        shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)
    
    @classmethod
    def from_dict(self, data):
        width = data.get("width", 1.0)
        height = data.get("height", 1.0)
        depth = data.get("depth", 1.0)
        return Box(width, height, depth)
