import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from pyrr import Matrix44
from scene.component.components.mesh_renderer import MeshRenderer


class RenderManager:
    def __init__(self):
        self.meshes = []

    def add_mesh(self, mesh_renderer: MeshRenderer):
        self.meshes.append(mesh_renderer)

    def render_all(self, view_matrix: Matrix44, projection_matrix: Matrix44, light_dir=(1.0, 1.0, 1.0)):
        for mesh in self.meshes:
            mesh.render(view_matrix, projection_matrix, light_dir)
