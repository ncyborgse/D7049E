import pybullet as p
from collision.shapes.shape import Shape


class Cylinder(Shape):
    def __init__(self, height=1.0, radius=0.5):

        super().__init__()
        self.height = height
        self.radius = radius

    def get_type(self):
        return "Box"
    
    def to_dict(self):
        return {
            "type": self.get_type(),
            "height": self.height,
            "radius": self.radius
        }
    
    def create_shape(self):
        # Create a cylinder shape in PyBullet
        half_extents = [self.width / 2, self.height / 2, self.radius]
        shape_id = p.createCollisionShape(p.GEOM_CYLINDER, radius=self.radius, height=self.height)
        return shape_id
    
    @classmethod
    def from_dict(self, data):
        height = data.get("height", 1.0)
        radius = data.get("radius", 0.5)
        return Cylinder(height, radius)
