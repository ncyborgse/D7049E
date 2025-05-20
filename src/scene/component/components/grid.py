from readerwriterlock import rwlock
from scene.component.component import Component
from core.component_registry import register_component


@register_component
class Grid(Component):
    def __init__(self, name="Grid"):
        super().__init__(name=name)
        self.lock = rwlock.RWLockFair()

    def subscribe(self, event_emitter):
        pass

    def set_size(self, width, height):
        with self.lock.gen_wlock():
            if width <= 0 or height <= 0:
                raise ValueError("Width and height must be positive integers.")
            self.width = width
            self.height = height

    def get_size(self):
        with self.lock.gen_rlock():
            return self.width, self.height

    def set_tile_size(self, tile_w, tile_h):
        with self.lock.gen_wlock():
            if tile_w <= 0 or tile_h <= 0:
                raise ValueError("Tile width and height must be positive integers.")
            self.tile_width = tile_w
            self.tile_height = tile_h

    def get_tile_size(self):
        with self.lock.gen_rlock():
            return self.tile_width, self.tile_height
    
    def set_tile_neighbors(self, num_neighbors):
        with self.lock.gen_wlock():
            if num_neighbors <= 0:
                raise ValueError("Number of neighbors must be positive integers.")
            self.num_neighbors = num_neighbors

    def get_tile_neighbors(self):
        with self.lock.gen_rlock():
            return self.num_neighbors

    

    def to_dict(self):
        base = super().to_dict()
        base["width"] = self.width
        base["height"] = self.height
        base["tile_width"] = self.tile_width
        base["tile_height"] = self.tile_height
        base["num_neighbors"] = self.num_neighbors
        return base

    @classmethod
    def from_dict(cls, data, scene_manager):
        name = data.get("name", "Grid")
        grid = cls(name=name)
        grid.set_size(data.get("width", 10), data.get("height", 10))
        grid.set_tile_size(data.get("tile_width", 1), data.get("tile_height", 1))
        grid.set_tile_neighbors(data.get("num_neighbors", 4))
        return grid

                

    






    
