import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))    # Fix the import path

import time
import moderngl
import pyglet
import numpy as np #from pyrr import Matrix44
from scene.component.components.mesh_renderer import MeshRenderer


class RenderManager:
    def __init__(self, scene_manager, shutdown_event, game_manager=None):
        self.shutdown_event = shutdown_event
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.meshes = []

        self.window = pyglet.window.Window(800, 600, "New World", vsync=True)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.CULL_FACE)      # Enable backface culling
        self.ctx.enable(moderngl.DEPTH_TEST)     # Enable depth testing

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
            if mesh.not_created:
                mesh.create(self.ctx)
            mesh.render(view_matrix, projection_matrix, light_dir)

    def draw(self):
        #self.ctx.clear(0.2, 0.2, 0.2)

        
        if self.shutdown_event.is_set():
            pyglet.app.exit()
            return
        
        cameras = self.scene_manager.get_current_cameras()
        print(cameras)
        if len(cameras) != 1:
            raise ValueError("Expected exactly one camera in scene.")

        camera = cameras[0]
        view = self.look_at(camera.get_eye(), camera.get_target(), camera.get_up())
        self.ctx.clear(0.1, 0.1, 0.1)
        self.render_all(view, self.proj)
        self.window.flip()
        

        

    def update(self, dt):
        self.window.invalid = True

    def run(self):
        self.proj = self.perspective_projection(45.0, 800 / 600, 0.1, 100.0)

        @self.window.event
        def on_draw():
            self.draw()

        @self.window.event
        def on_close():
            self.shutdown_event.set()
            pyglet.app.exit()

        pyglet.clock.schedule_interval(lambda dt: self.window.dispatch_event('on_draw'), 1/60.0)
        pyglet.app.run()

        '''
        # Main loop for the render manager
        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600
        proj = self.perspective_projection(45.0, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)

        while not self.shutdown_event.is_set():

            cameras = self.scene_manager.get_current_cameras()

            print(cameras)

            if len(cameras) == 1:
                camera = cameras[0]
            elif len(cameras) > 1:
                raise ValueError("Multiple cameras found in the scene. Please ensure only one camera is present.")
            else:
                raise ValueError("No camera found in the scene. Please add a camera to the scene.")

            eye = camera.get_eye()
            target = camera.get_target()
            up = camera.get_up()

            view = self.look_at(eye, target, up)

            self.ctx.clear(0.1, 0.1, 0.1)
            self.render_all(view, proj)

            # Sleep for a short duration to limit the frame rate
            #time.sleep(1.0 / 60)    # frame_rate = 60
            self.window.flip()    # Swap the buffers to display the rendered frame
            pyglet.clock.tick()

        '''