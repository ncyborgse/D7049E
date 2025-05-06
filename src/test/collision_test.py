from scene.component.components.script import Script
from scene.scene_graph import SceneGraph
from core.scene_manager import SceneManager
from scene.objects.node import Node
from scene.component.components.collider import Collider
from collision.shape.shapes.box import Box
from collision.collision_manager import CollisionManager
import numpy as np

from pyee import EventEmitter
from core.engine import Engine



scene_manager = SceneManager()

engine_api = {
    "SceneManager" : {
        "load_scene" : scene_manager.load_scene,
        "get_current_scene" : scene_manager.get_current_scene,
        "get_scenes" : scene_manager.get_scenes,
    }
}

scene_graph = SceneGraph(name="Scene1")

scene_manager.add_scene(scene_graph)
scene_manager.load_scene("Scene1")



emitter = EventEmitter()


src = "src/test/testScript.lua"
script1 = Script("Script1")
script1.attach_script(src, engine_api)

collision_manager = CollisionManager(scene_manager)

collider = Collider()
collider2 = Collider()



node1 = Node("Node1", transform  = np.identity(4))
node1.add_component(script1)
node1.add_component(collider)

node2 = Node("Node2", transform = np.identity(4))
node2.add_component(collider2)

scene_graph.add_node(node1)
scene_graph.add_node(node2)

collision_manager.register_colliders()

collider.set_shape(Box(1, 1, 1))
transform = np.identity(4)
transform[0, 3] = 0.1
transform[1, 3] = 0.1
transform[2, 3] = 0.1
collider.set_transform(transform)

collider2.set_shape(Box(1, 1, 1))
collider2.set_transform(np.identity(4))

root = scene_graph.get_root()


collision_manager.check_collisions()




