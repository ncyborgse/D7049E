import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))    # Fix the import path

import time
import numpy as np #from pyrr import Matrix44
from scene.component.components.mesh_renderer import MeshRenderer


class RenderManager:
    def __init__(self, scene_manager, game_manager):
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.meshes = []


    def add_mesh(self, mesh_renderer: MeshRenderer):
        self.meshes.append(mesh_renderer)

    def remove_mesh(self, mesh_renderer: MeshRenderer):
        if mesh_renderer in self.meshes:
            self.meshes.remove(mesh_renderer)
        else:
            raise ValueError("MeshRenderer not found in RenderManager.")


    def register_mesh_renderers(self):
        for scene in self.scene_manager.get_scenes():
            root = scene.get_root()
            nodes_to_check = [root]

            while nodes_to_check:
                current_node = nodes_to_check.pop()
                mesh = current_node.get_component("MeshRenderer")
                if mesh:
                    self.add_mesh(mesh)

                # Add children to the list for further checking
                for child in current_node.get_children():
                    nodes_to_check.append(child)


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


    def render_all(self, view_matrix, projection_matrix, light_dir=(1.0, 1.0, 1.0), delta_time=None):
        for mesh in self.meshes:
            mesh.render(view_matrix, projection_matrix, light_dir)


    def run(self):
        # Main loop for the render manager
        self.is_running = True
        previous_time = time.time()

        while self.is_running:
            current_time = time.time()
            delta_time = current_time - previous_time
            previous_time = current_time

            camera = self.game_manager.get_camera()
            if camera is None:
                raise ValueError("Camera not found in GameManager.")

            eye = camera.get_eye()
            target = camera.get_target()
            up = camera.get_up()

            window = self.game_manager.get_window()
            if window is None:
                raise ValueError("Window not found in GameManager.")

            view = self.look_at(eye, target, up)
            proj = self.perspective_projection(45.0, window.width / window.height, 0.1, 100.0)

            self.render_all(view, proj)

            # Sleep for a short duration to limit the frame rate
            time.sleep(1.0 / 60)    # frame_rate = 60

    def stop(self):
        self.is_running = False
