import numpy as np
from scene.objects.node import Node
from scene.component.components.tile import Tile
from scene.component.components.mesh_renderer import MeshRenderer
from core.global_scene_manager import scene_manager
from readerwriterlock import rwlock

import heapq
import itertools

class GridSystem:
    def __init__(self):
        self.grid = None
        self.lock = rwlock.RWLockFair()

    def set_grid(self, grid):
        with self.lock.gen_wlock():
            self.grid = grid

    def get_grid(self):
        with self.lock.gen_rlock():
            return self.grid

    def update_grid(self, width, height, tile_edges=4, tile_height=1, tile_width=1):
        if self.get_grid() is None:
            raise ValueError("Grid is not set. Please set the grid before updating.")
        # Create tiles as children to the parent node

        with self.lock.gen_wlock():
            self.grid.set_size(width, height)
            self.grid.set_tile_size(tile_width, tile_height)
            self.grid.set_tile_neighbors(tile_edges)

        # Remove all current child tiles

        

        for child in self.get_grid().get_parent().get_children():
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
        if self.get_grid() is None:
            raise ValueError("Grid is not set. Please set the grid before checking visibility.")

        # Search cardinal directions for tile2 from tile1

        for i in range(4):
            tile = tile1
            while tile.get_neighbors()[i] is not None and tile.get_neighbors()[i].is_see_through():
                if tile.get_neighbors()[i] == tile2:
                    return True
                tile = tile.get_neighbors()[i]
        
        return False
    
    def distance(self, tile1, tile2):
        if self.grid is None:
            raise ValueError("Grid is not set. Please set the grid before calculating distance.")
        if tile1==tile2:
            return 0
        
        # Get the distance between two tiles regardless of visibility/movement cost

        coords = tile1.get_coords()
        coords2 = tile2.get_coords()    

        return abs(coords[0] - coords2[0]) + abs(coords[1] - coords2[1])

    def navigate(self, tile1, tile2):
        if self.grid is None:
            raise ValueError("Grid is not set. Please set the grid before navigating.")
        if tile1==tile2:
            return [tile1]
        
        # A* pathfinding algorithm


        open_set = []
        counter = itertools.count()
        heapq.heappush(open_set, (0, next(counter), tile1)) # Tie breaker counter
        visited = set()

        came_from = {}
        g_score = {tile1: 0} 
        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current in visited:
                continue
            visited.add(current)

            if current == tile2:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            
            for neighbor in current.get_neighbors():
                if neighbor is None:
                    continue
                move_cost = neighbor.get_movement_cost()
                new_cost = g_score[current] + move_cost

                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost, next(counter), neighbor))

        return None
    
    def connect_grid(self):
        # Find grid objects in all scenes

        # Ensure there is only one grid per scene
        scenes = scene_manager.get_scenes()
        for scene in scenes:
            root = scene.get_root()
            nodes_to_check = [root]
            grids = []
            while nodes_to_check:
                current_node = nodes_to_check.pop()
                grid = current_node.get_component("Grid")
                if grid:
                    grids.append(grid)

                # Add children to the list for further checking

                for child in current_node.get_children():
                    nodes_to_check.append(child)

            if len(grids) > 1:
                raise ValueError("Only one grid per scene is supported.")
            if not grids:
                break
            grid = grids[0]
            
            width, height = grid.get_size()
            num_neighbors = grid.get_tile_neighbors()

            if num_neighbors != 4:
                raise ValueError("Only 4 edges are supported for now.")
            
            children = grid.get_parent().get_children()

            tiles = []

            for child in children:
                child.get_components()
                for component in child.get_components():
                    if isinstance(component, Tile):
                        tiles.append(component)
                        break


            # Attach tiles to neighboring nodes

            # Assuming order of tiles is preserved when loaded 

            # Instead, sort by x and y coordinates to ensure correct order

            tiles.sort(key=lambda tile: (tile.get_coords()[0], tile.get_coords()[1]))

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



            
            









         
        

    