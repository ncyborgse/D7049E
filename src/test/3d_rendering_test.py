import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import numpy as np #from pyrr import Matrix44

from core.scene_manager import SceneManager
from core.render_manager import RenderManager
from core.global_scene_manager import scene_manager

from scene.scene_graph import SceneGraph
from scene.objects.node import Node
from scene.component.components.mesh_renderer import MeshRenderer
import threading
from scene.component.components.camera import Camera



shutdown_event = threading.Event()
# Create a scene manager and render manager

render_manager = RenderManager(scene_manager, shutdown_event)

scene_graph = SceneGraph(name="Scene1")
scene_manager.add_scene(scene_graph)

node1 = Node("Node1", parent=None)
node2 = Node("Node2", parent=node1)
node3 = Node("Node3", transform=np.identity(4))

# Create mesh renderers and add them to the nodes
vertices = np.array([
    -1, -1, -1,
    1, -1, -1,
    1,  1, -1,
    -1,  1, -1,
    -1, -1,  1,
    1, -1,  1,
    1,  1,  1,
    -1,  1,  1

], dtype='f4')

vertices = np.array(vertices, dtype='f4').reshape(-1, 3)  # Reshape to (n, 3) where n is the number of vertices

indices = np.array([    
    0, 3, 1, 3, 2, 1,
    1, 2, 5, 2, 6, 5,
    5, 6, 4, 6, 7, 4,
    4, 7, 0, 7, 3, 0,
    3, 7, 2, 7, 6, 2,
    4, 0, 5, 0, 1, 5], dtype='i4')

mesh1 = MeshRenderer(vertices=vertices, indices=indices)
mesh2 = MeshRenderer(vertices=vertices, indices=indices)
camera = Camera()
camera.set_eye([0, -5, -5])
camera.set_target([0, 0, 0])
node1.add_component(mesh1)
node2.add_component(mesh2)
node3.add_component(camera)

scene_graph.add_node(node1)
scene_graph.add_node(node2)
scene_graph.add_node(node3)



# Set the transforms for the nodes
# Note: The transforms are in column-major order for OpenGL
transform1 = np.array([
    [ 0.5, 0.0, 0.0, 0],
    [ 0.0, 0.5, 0.0, 0],
    [ 0.0, 0.0, 0.5, 0],
    [ 0.0, 0.0, 0.0, 1]
], dtype='f4')  # or dtype='float32'
transform2 = np.array([
    [ 1, 0, 0,  -3],
    [ 0, 1, 0,  0],
    [ 0, 0, 1,  0],
    [ 0, 0, 0,  1]
], dtype='f4')  # or dtype='float32'

# Set the local transforms for the nodes
node1.set_local_transform(transform1)
node2.set_local_transform(transform2)

# Update the transforms of the mesh renderers
mesh1.set_transform(np.identity(4))
mesh2.set_transform(np.identity(4))

scene_manager.load_scene("Scene1")  # Load the scene into the scene manager to update tracked cameras

render_manager.register_mesh_renderers()    # find all mesh renderers in the scene graph and add them to the render manager

render_manager.run()

