import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import moderngl
import pyglet
import numpy as np #from pyrr import Matrix44

from core.scene_manager import SceneManager
from core.render_manager import RenderManager

from scene.scene_graph import SceneGraph
from scene.objects.node import Node
from scene.component.components.mesh_renderer import MeshRenderer



# Create a pyglet window
window = pyglet.window.Window(800, 600, "MeshRenderer Test")

# Create ModernGL context
ctx = moderngl.create_context()

# Set up the OpenGL context and shaders
ctx.enable(moderngl.CULL_FACE)      # Enable backface culling
ctx.enable(moderngl.DEPTH_TEST)     # Enable depth testing

# Create a scene manager and render manager
scene_manager = SceneManager()
render_manager = RenderManager(scene_manager)

scene_graph = SceneGraph()
scene_manager.add_scene(scene_graph)

node1 = Node("Node1", parent=scene_graph.get_root())
node2 = Node("Node2", parent=node1)

# Create mesh renderers and add them to the nodes
mesh1 = MeshRenderer(ctx, "../../assets/models/Trollboyobj.obj")
mesh2 = MeshRenderer(ctx, "../../assets/models/banana duck.obj")
node1.add_component(mesh1)
node2.add_component(mesh2)

# Set the transforms for the nodes
# Note: The transforms are in column-major order for OpenGL
transform1 = np.array([
    [ 0.5, 0.0, 0.0,  -5],
    [ 0.0, 0.5, 0.0, -10],
    [ 0.0, 0.0, 0.5,   0],
    [ 0.0, 0.0, 0.0,   1]
], dtype='f4')  # or dtype='float32'
transform2 = np.array([
    [ 1, 0, 0,  0],
    [ 0, 1, 0, -5],
    [ 0, 0, 1,  0],
    [ 0, 0, 0,  1]
], dtype='f4')  # or dtype='float32'

# Set the local transforms for the nodes
node1.set_local_transform(transform1)
node2.set_local_transform(transform2)

# Update the transforms of the mesh renderers
mesh1.set_transform(np.identity(4))
mesh2.set_transform(np.identity(4))

render_manager.register_mesh_renderers()    # find all mesh renderers in the scene graph and add them to the render manager


@window.event
def on_draw():
    ctx.clear(0.1, 0.1, 0.1)

    # Create view and projection matrices

    view = render_manager.look_at( (5.0, 7.0, 6.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
    #view = Matrix44.look_at(
    #    eye=(5.0, 7.0, 6.0),
    #    target=(0.0, 0.0, 0.0),
    #    up=(0.0, 1.0, 0.0)
    #)

    proj = render_manager.perspective_projection(45.0, window.width / window.height, 0.1, 100.0)
    #proj = Matrix44.perspective_projection(45.0, window.width / window.height, 0.1, 100.0)

    # Render all meshes
    render_manager.render_all(view, proj, light_dir=(1.0, 1.0, 1.0))

# Run the application
pyglet.app.run()
