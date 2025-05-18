import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import numpy as np #from pyrr import Matrix44
from core.render_manager import RenderManager
from core.global_scene_manager import scene_manager
from core.grid_system import GridSystem

from scene.scene_graph import SceneGraph
from scene.objects.node import Node
from scene.component.components.grid import Grid
import threading
from scene.component.components.camera import Camera




shutdown_event = threading.Event()
# Create a scene manager and render manager

render_manager = RenderManager(scene_manager, shutdown_event)

scene_graph = SceneGraph(name="Scene1")
scene_manager.add_scene(scene_graph)

node1 = Node("Node1")

camera_node = Node("CameraNode")

grid = Grid()
node1.add_component(grid)

grid_system = GridSystem()
grid_system.set_grid(grid)
grid_system.update_grid(4, 5, tile_edges = 4, tile_height=1, tile_width=1)

camera = Camera()
camera.set_eye([0, -5, -5])
camera.set_target([0, 0, 0])

camera_node.add_component(camera)

scene_graph.add_node(node1)
scene_graph.add_node(camera_node)



# Set the transforms for the nodes
# Note: The transforms are in column-major order for OpenGL


scene_manager.load_scene("Scene1")  # Load the scene into the scene manager to update tracked cameras

render_manager.register_mesh_renderers()    # find all mesh renderers in the scene graph and add them to the render manager

render_manager.run()

