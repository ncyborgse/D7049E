import numpy as np
from scene.objects.node import Node
from scene.component.components.tile import Tile
from scene.component.components.mesh_renderer import MeshRenderer


class GridSystem:
    def __init__(self):
        self.grid = None

    def set_grid(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid

    def update_grid(self, width, height, tile_edges=4, tile_height=1, tile_width=1):
        if self.grid is None:
            raise ValueError("Grid is not set. Please set the grid before updating.")
        # Create tiles as children to the parent node
        
        # Remove all current child tiles

        for child in self.grid.get_parent().get_children():
            child.get_components()
            for component in child.get_components():
                if isinstance(component, Tile):
                    child.detach()
                    break


        # Create new tiles, would ideally be done with shape support later

        # Support for 4 edges only for now
        if tile_edges not in [4]:
            raise ValueError("Only 4 edges are supported for now.")
        

        tiles = []
        for i in range(width):
            for j in range(height):
                node = Node(name=f"Tile<{i}, {j}>", parent=self.grid.get_parent())
                tile = Tile(x=i, y=j, num_neighbors=4)

                w = tile_width/2
                h = tile_height/2
                t = 0.2

                vertices = np.array([
                    -w, -h, -t,
                    w, -h, -t,
                    w,  h, -t,
                    -w,  h, -t,
                    -w, -h,  t,
                    w, -h,  t,
                    w,  h,  t,
                    -w,  h,  t

                    ], dtype='f4')

                vertices = np.array(vertices, dtype='f4').reshape(-1, 3)  # Reshape to (n, 3) where n is the number of vertices

                indices = np.array([    
                    0, 3, 1, 3, 2, 1,
                    1, 2, 5, 2, 6, 5,
                    5, 6, 4, 6, 7, 4,
                    4, 7, 0, 7, 3, 0,
                    3, 7, 2, 7, 6, 2,
                    4, 0, 5, 0, 1, 5], dtype='i4')
                
                mesh = MeshRenderer(vertices=vertices, indices=indices)

                transform = np.array([
                    [1, 0, 0, i * tile_width],
                    [0, 1, 0, j * tile_height],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]
                ], dtype='f4')

                node.set_local_transform(transform)
                node.add_component(mesh)
                node.add_component(tile)
                tiles.append(tile)

        # Attach tiles to neighboring nodes

        # Indices are 0 = left, 1 = up, 2 = right, 3 = down

        for i in range(width):
            for j in range(height):
                tile = tiles[i * height + j]

                if i > 0:
                    tile.add_neighbor(tiles[(i - 1) * height + j], 0)
                if j < height - 1:
                    tile.add_neighbor(tiles[i * height + (j + 1)], 1)
                if i < width - 1:
                    tile.add_neighbor(tiles[(i + 1) * height + j], 2)
                if j > 0:
                    tile.add_neighbor(tiles[i * height + (j - 1)], 3)

    
    def is_visible(self, tile1, tile2):
        if self.grid is None:
            raise ValueError("Grid is not set. Please set the grid before checking visibility.")
    
    def navigate(self, tile1, tile2):
        if self.grid is None:
            raise ValueError("Grid is not set. Please set the grid before navigating.")
        # Implement navigation logic here
        pass
        

    