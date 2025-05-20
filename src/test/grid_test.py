import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import numpy as np #from pyrr import Matrix44
from core.render_manager import RenderManager
from core.global_scene_manager import scene_manager
from core.grid_system import GridSystem
from core.state_manager import StateManager

from scene.scene_graph import SceneGraph
from scene.objects.node import Node
from scene.component.components.grid import Grid
import threading
from scene.component.components.camera import Camera
from scene.component.components.script import Script



engine_api = {
    "SceneManager" : {
        "load_scene" : scene_manager.load_scene,
        "get_current_scene" : scene_manager.get_current_scene,
        "get_scenes" : scene_manager.get_scenes,
        "get_current_cameras" : scene_manager.get_current_cameras,
    }
}
src = "src/test/camera_movement.lua"


shutdown_event = threading.Event()
# Create a scene manager and render manager

render_manager = RenderManager(scene_manager, shutdown_event)

scene_graph = SceneGraph(name="Scene1")
scene_manager.add_scene(scene_graph)

state_manager = StateManager()
state_manager.set_scene_manager(scene_manager)

state_manager.new_project("GridTestProject")
state_manager.load_project("GridTestProject")

node1 = Node("Node1")

camera_node = Node("CameraNode")

grid = Grid()
node1.add_component(grid)

grid_system = GridSystem()
grid_system.set_grid(grid)
grid_system.update_grid(4, 5, tile_edges = 4, tile_height=1, tile_width=1)

camera = Camera()
camera.set_eye([0, -5, -6])
camera.set_target([0, 0, 0])

camera_script = Script()
camera_script.attach_script(src, engine_api)

camera_node.add_component(camera_script)

camera_node.add_component(camera)

scene_graph.add_node(node1)
scene_graph.add_node(camera_node)

tiles = grid.get_parent().get_children()

first_tile = tiles[0].get_components()[1]
last_tile = tiles[-1].get_components()[1]

for child in tiles:
    child.get_components()
    for component in child.get_components():
        if component.get_name() == "Tile<1, 3>" or component.get_name() == "Tile<2, 3>" or component.get_name() == "Tile<3, 3>" or component.get_name() == "Tile<0, 1>":
            component.set_movement_cost(100)

path = grid_system.navigate(first_tile, last_tile)

totalCost = 0
print("Path from first tile to last tile:")
for tile in path:
    print(tile.get_name())
    print(tile.get_movement_cost())
    totalCost += tile.get_movement_cost()

print("Total cost of the path:", totalCost)

# Set the transforms for the nodes
# Note: The transforms are in column-major order for OpenGL

state_manager.save_project()
