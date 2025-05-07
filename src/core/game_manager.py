from core.engine import Engine
from core.state_manager import StateManager
from core.global_scene_manager import scene_manager
from core.render_manager import RenderManager
from collision.collision_manager import CollisionManager
import threading

class GameManager:
    def __init__(self):
        self.shutdown_event = threading.Event()
        self.threads = []

    def run(self):
        # Start the engine loop, rendering and collision detection (maybe audio in the future) in separate threads
        self.engine = Engine(scene_manager, self.shutdown_event)
        self.render_manager = RenderManager(scene_manager, self.shutdown_event)
        self.collision_manager = CollisionManager(scene_manager, self.shutdown_event)
        
        self.render_manager.register_mesh_renderers()
        self.collision_manager.register_colliders()

        self.threads = [
            threading.Thread(target=self.engine.run),
            threading.Thread(target=self.render_manager.run),
            threading.Thread(target=self.collision_manager.run)
        ]

        for thread in self.threads:
            thread.start()

        try:
            for t in self.threads:
                t.join()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.shutdown_event.set()

        for thread in self.threads:
            thread.join()
