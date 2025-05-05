import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))    # Fix the import path

import numpy as np #from pyrr import Matrix44
from scene.component.components.mesh_renderer import MeshRenderer


class RenderManager:
    def __init__(self):
        self.meshes = []


    def add_mesh(self, mesh_renderer: MeshRenderer):
        self.meshes.append(mesh_renderer)

    def remove_mesh(self, mesh_renderer: MeshRenderer):
        if mesh_renderer in self.meshes:
            self.meshes.remove(mesh_renderer)
        else:
            raise ValueError("MeshRenderer not found in RenderManager.")


    def render_all(self, view_matrix, projection_matrix, light_dir=(1.0, 1.0, 1.0)):
        for mesh in self.meshes:
            mesh.render(view_matrix, projection_matrix, light_dir)



    def perspective_projection(self, fov_deg, aspect, near, far):
        f = 1.0 / np.tan(np.radians(fov_deg) / 2.0)
        proj = np.zeros((4, 4), dtype='f4')

        proj[0, 0] = f / aspect
        proj[1, 1] = f
        proj[2, 2] = (far + near) / (near - far)
        proj[2, 3] = (2 * far * near) / (near - far)
        proj[3, 2] = -1.0
        return proj

    def look_at(self, eye, target, up):
        eye = np.array(eye, dtype='f4')
        target = np.array(target, dtype='f4')
        up = np.array(up, dtype='f4')

        f = target - eye
        f = f / np.linalg.norm(f)

        u = up / np.linalg.norm(up)
        s = np.cross(f, u)
        s = s / np.linalg.norm(s)
        u = np.cross(s, f)

        view = np.identity(4, dtype='f4')
        view[0, :3] = s
        view[1, :3] = u
        view[2, :3] = -f
        view[:3, 3] = -np.dot(view[:3, :3], eye)
        return view
