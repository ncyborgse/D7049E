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

    def initialize(self, width, height, tile_edges, tile_height, tile_width):
        # Create tiles as children to the parent node
        pass