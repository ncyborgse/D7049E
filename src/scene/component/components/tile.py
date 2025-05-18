from readerwriterlock import rwlock
from scene.component.component import Component
from core.component_registry import register_component

@register_component
class Tile(Component):
    def __init__(self, x,y, num_neighbors):
        super().__init__(name="Tile<" + str(x) + ", " + str(y) + ">")
        self.lock = rwlock.RWLockFair()
        self.num_neighbors = num_neighbors
        self.x = x
        self.y = y
        self.neighbors = []
        self.movement_cost = 1.0
        self.see_through = True

    def subscribe(self, event_emitter):
        pass

    def add_neighbor(self, neighbor, index):
        if index < 0 or index >= self.num_neighbors:
            raise IndexError("Index out of bounds for neighbors.")
        with self.lock.gen_wlock():
            self.neighbors[index] = neighbor
    
    def get_neighbors(self):
        with self.lock.gen_rlock():
            return self.neighbors.copy()

    def set_neighbors(self, neighbors):
        with self.lock.gen_wlock():
            if len(neighbors) != self.num_neighbors:
                raise ValueError("Number of neighbors must match the initialized number.")
            self.neighbors = neighbors.copy()
        
    def get_movement_cost(self):
        with self.lock.gen_rlock():
            return self.movement_cost
        
    def set_movement_cost(self, cost):
        with self.lock.gen_wlock():
            if cost < 0:
                raise ValueError("Movement cost cannot be negative.")
            self.movement_cost = cost

    def is_see_through(self):
        with self.lock.gen_rlock():
            return self.see_through
        
    def set_see_through(self, see_through):
        with self.lock.gen_wlock():
            self.see_through = see_through

    def get_coords(self):
        with self.lock.gen_rlock():
            return (self.x, self.y)

    def to_dict(self):
        base = super().to_dict()
        base["x"] = self.x
        base["y"] = self.y
        base["num_neighbors"] = self.num_neighbors
        base["movement_cost"] = self.movement_cost
        base["see_through"] = self.see_through
        return base
    
    @classmethod
    def from_dict(cls, data, scene_manager):
        x = data.get("x", 0)
        y = data.get("y", 0)
        num_neighbors = data.get("num_neighbors", 4)
        movement_cost = data.get("movement_cost", 1.0)
        see_through = data.get("see_through", True)
        tile = cls(x, y, num_neighbors)
        tile.set_movement_cost(movement_cost)
        tile.set_see_through(see_through)
        return tile