import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import numpy as np #from pyrr import Matrix44
from core.render_manager import RenderManager
from core.global_scene_manager import scene_manager
from core.grid_system import GridSystem
from core.state_manager import StateManager

from scene.component.components.mesh_renderer import MeshRenderer
from scene.objects.node import Node
from scene.component.components.grid import Grid
import threading
from scene.component.components.camera import Camera
from scene.component.components.script import Script
from scene.component.components.attacker import Attacker
from scene.component.components.attackable import Attackable
from scene.component.components.collider import Collider
from scene.component.components.clickable import Clickable
from collision.shape.shapes.box import Box



engine_api = {
    "SceneManager" : {
        "load_scene" : scene_manager.load_scene,
        "get_current_scene" : scene_manager.get_current_scene,
        "get_scenes" : scene_manager.get_scenes,
        "get_current_cameras" : scene_manager.get_current_cameras,
    }
}
src1 = "camera_movement.lua"
src2 = "goblinScript.lua"
src3 = "bananaScript.lua"


shutdown_event = threading.Event()
# Create a scene manager and render manager

render_manager = RenderManager(scene_manager, shutdown_event)

state_manager = StateManager()
state_manager.set_scene_manager(scene_manager)

#state_manager.new_project("AttackerTestProject")
state_manager.load_project("AttackerTestProject")

scene_graph = scene_manager.get_current_scene()

node1 = Node("Node1")

grid = Grid()
node1.add_component(grid)

grid_system = GridSystem()
grid_system.set_grid(grid)
grid_system.update_grid(4, 5, tile_edges = 4, tile_height=1, tile_width=1)

camera = Camera()
camera.set_eye([0, -5, -6])
camera.set_target([0, 0, 0])

camera_node = Node("CameraNode")

camera_script = Script()
camera_script.attach_script(src1, engine_api)

camera_node.add_component(camera_script)
camera_node.add_component(camera)

goblinNode = Node("GoblinNode")

goblin_mesh = MeshRenderer(obj_path="Trollboyobj.obj")
goblin_script = Script()
goblin_script.attach_script(src2, engine_api)
goblin_attacker = Attacker()

goblinNode.add_component(goblin_mesh)
goblinNode.add_component(goblin_script)
goblinNode.add_component(goblin_attacker)

# Shrink and rotate goblin
shrinkTransform = np.array([
    0.2, 0, 0, 0,
    0, 0.2, 0, 0,
    0, 0, 0.2, 0,
    0, 0, 0, 1
], dtype='f4').reshape(4, 4)

theta = -np.pi/2

rotationTransformZ = np.array([
    np.cos(theta), -np.sin(theta), 0, 0,
    np.sin(theta), np.cos(theta), 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1
], dtype='f4').reshape(4, 4)

rotationTransformY = np.array([
    np.cos(theta), 0, np.sin(theta), 0,
    0, 1, 0, 0,
    -np.sin(theta), 0, np.cos(theta), 0,
    0, 0, 0, 1
], dtype='f4').reshape(4, 4)

theta = np.pi/2

rotationTransformX = np.array([
    1, 0, 0, 0,
    0, np.cos(theta), -np.sin(theta), 0,
    0, np.sin(theta), np.cos(theta), 0,
    0, 0, 0, 1
], dtype='f4').reshape(4, 4)


transform = np.dot(rotationTransformZ, shrinkTransform)
transform = np.dot(rotationTransformY, transform)
transform = np.dot(rotationTransformY, transform)
transform = np.dot(rotationTransformY, transform)

print("Transform: ", transform)
goblinNode.apply_transform(transform)

bananaNode = Node("BananaNode")

banana_mesh = MeshRenderer(obj_path="banana duck.obj")
banana_script = Script()
banana_script.attach_script(src3, engine_api)
banana_attackable = Attackable()
banana_collider = Collider()
banana_clickable = Clickable()
banana_collider.set_shape(Box(1, 1, 1))

shrinkTransform = np.array([
    0.5, 0, 0, 0,
    0, 0.5, 0, 0,
    0, 0, 0.5, 0,
    0, 0, 0, 1
], dtype='f4').reshape(4, 4)

transform = np.dot(rotationTransformZ, shrinkTransform)
transform = np.dot(rotationTransformY, transform)
transform = np.dot(rotationTransformY, transform)
transform = np.dot(rotationTransformY, transform)

bananaNode.apply_transform(transform)

bananaNode.add_component(banana_mesh)
bananaNode.add_component(banana_script)
bananaNode.add_component(banana_attackable)
bananaNode.add_component(banana_collider)
bananaNode.add_component(banana_clickable)


scene_graph.add_node(node1)
scene_graph.add_node(camera_node)
scene_graph.add_node(goblinNode)
scene_graph.add_node(bananaNode)

tiles = grid.get_parent().get_children()

first_tile = tiles[0]
last_tile = tiles[-1]

# Put banana in the first tile and goblin in the last tile

bananaNode.attach(first_tile)
goblinNode.attach(last_tile)


# Set the transforms for the nodes
# Note: The transforms are in column-major order for OpenGL

state_manager.save_project()
