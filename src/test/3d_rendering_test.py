import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import moderngl
import pyglet
from pyrr import Matrix44
from scene.component.components.mesh_renderer import MeshRenderer
from core.render_manager import RenderManager


# Create a pyglet window
window = pyglet.window.Window(800, 600, "MeshRenderer Test")

# Create ModernGL context
ctx = moderngl.create_context()

# Initialize render manager and load a mesh
ctx.enable(moderngl.CULL_FACE)  # Enable backface culling
ctx.enable(moderngl.DEPTH_TEST)  # Enable depth testing
render_manager = RenderManager()
mesh1 = MeshRenderer(ctx, "../../assets/models/Trollboyobj.obj")
mesh2 = MeshRenderer(ctx, "../../assets/models/banana duck.obj")
render_manager.add_mesh(mesh1)
render_manager.add_mesh(mesh2)

# Optional: move the mesh to a different position
mesh1.set_model_matrix(Matrix44.from_translation([-5, -15, -10]))
mesh2.set_model_matrix(Matrix44.from_translation([0, -15, -10]))

@window.event
def on_draw():
    ctx.clear(0.1, 0.1, 0.1)
    
    # Create view and projection matrices
    view = Matrix44.look_at(
        eye=(5.0, 7.0, 6.0),
        target=(0.0, 0.0, 0.0),
        up=(0.0, 1.0, 0.0)
    )
    proj = Matrix44.perspective_projection(45.0, window.width / window.height, 0.1, 100.0)

    # Render all meshes
    render_manager.render_all(view, proj, light_dir=(1.0, 1.0, 1.0))

# Run the application
pyglet.app.run()
