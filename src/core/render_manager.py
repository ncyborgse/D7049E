import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))    # Fix the import path

import time
import moderngl
import pyglet
import numpy as np #from pyrr import Matrix44
from scene.component.components.mesh_renderer import MeshRenderer
from core.global_scene_manager import scene_manager


class RenderManager:
    def __init__(self, scene_manager, shutdown_event, game_manager=None):
        self.shutdown_event = shutdown_event
        self.scene_manager = scene_manager
        self.game_manager = game_manager
        self.meshes = []
        self.prev_keys = []

        self.window = pyglet.window.Window(800, 600, "New World", vsync=True)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.CULL_FACE)      # Enable backface culling
        #self.ctx.disable(moderngl.CULL_FACE)    # Disable backface culling
        self.ctx.enable(moderngl.DEPTH_TEST)     # Enable depth testing

    def add_mesh(self, mesh_renderer: MeshRenderer):
        self.meshes.append(mesh_renderer)

    def remove_mesh(self, mesh_renderer: MeshRenderer):
        if mesh_renderer in self.meshes:
            self.meshes.remove(mesh_renderer)
        else:
            raise ValueError("MeshRenderer not found in RenderManager.")

    def set_collision_manager(self, collision_manager):
        self.collision_manager = collision_manager


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


    def render_all(self, view_matrix, projection_matrix, light_dir=(0, 0, -5), delta_time=None):
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
        if len(cameras) != 1:
            raise ValueError("Expected exactly one camera in scene.")

        camera = cameras[0]
        view = self.look_at(camera.get_eye(), camera.get_target(), camera.get_up())
        self.ctx.clear(0.2, 0.2, 0.2)
        self.render_all(view, self.proj)
        self.window.flip()
        

    def update(self, dt):
        
        curr_keys = []

        root = scene_manager.get_current_scene().get_root()

        for k in self._all_keys():
            if self.keys[k]:
                key = pyglet.window.key.symbol_string(k)
                curr_keys.append(key)

        #print("Keys pressed: " + str(curr_keys))
        for key in curr_keys:
            if key not in self.prev_keys:
                root.call_event_rec("onKeyPress", key)
            else:
                root.call_event_rec("onKeyHold", key, dt)
        
        for key in self.prev_keys:
            if key not in curr_keys:
                root.call_event_rec("onKeyRelease", key)

        self.prev_keys = curr_keys

        
        
        
        
    def _all_keys(self):
        return [getattr(pyglet.window.key, k) for k in dir(pyglet.window.key) if not k.startswith('__') and not k.startswith('_') and isinstance(getattr(pyglet.window.key, k), int)]


        

    def run(self):
        self.proj = self.perspective_projection(45.0, 800 / 600, 0.1, 100.0)

        @self.window.event
        def on_draw():
            self.draw()

        @self.window.event
        def on_close():
            self.shutdown_event.set()
            pyglet.app.exit()
        '''
        @self.window.event
        def on_key_press(symbol, modifiers):
            if self.engine is None:
                raise ValueError("Engine not set, cannot handle key press events.")
            # Convert symbol to string for easier handling
            key = pyglet.window.key.symbol_string(symbol)
            self.engine.queue_key_event(key, release = False)

        @self.window.event
        def on_key_release(symbol, modifiers):
            if self.engine is None:
                raise ValueError("Engine not set, cannot handle key press events.")
            key = pyglet.window.key.symbol_string(symbol)
            self.engine.queue_key_event(key, release = True)
        ''' 

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == pyglet.window.mouse.LEFT:
                # Queue click event to the collision manager
                if not self.collision_manager:
                    raise ValueError("Collision manager not set. Please set the collision manager before running.")
                ncd_x = (x / self.window.width) * 2 - 1 
                ncd_y = (y / self.window.height) * 2 - 1
                camera = self.scene_manager.get_current_cameras()[0]
                view_matrix = self.look_at(camera.get_eye(), camera.get_target(), camera.get_up())
                projection_matrix = self.perspective_projection(45.0, self.window.width / self.window.height, 0.1, 100.0)
                inv_view_proj = np.linalg.inv(np.dot(projection_matrix, view_matrix))

                near = np.array([ncd_x, ncd_y, 0.0, 1.0])
                far = np.array([ncd_x, ncd_y, 1.0, 1.0])

                near_world = np.dot(inv_view_proj, near)
                far_world = np.dot(inv_view_proj, far)

                near_world /= near_world[3]
                far_world /= far_world[3]

                ray_from = near_world[:3]
                ray_to = far_world[:3]
                self.collision_manager.queue_click_event(ray_from, ray_to)

        pyglet.clock.schedule_interval(lambda dt: self.window.dispatch_event('on_draw'), 1/60.0)
        pyglet.clock.schedule_interval(self.update, 1/300.0)  # Update every 1/60 seconds
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