import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from core.global_scene_manager import scene_manager
from scene.component.components.script import Script
from scene.component.components.collider import Collider
from scene.component.components.mesh_renderer import MeshRenderer
from collision.shape.shapes.box import Box
from scene.scene_graph import SceneGraph
from scene.component.components.camera import Camera
from scene.component.components.clickable import Clickable
from scene.objects.node import Node
from core.game_manager import GameManager

import numpy as np
#import moderngl

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


src = "testScript.lua"
script1 = Script("Script1")


script1.attach_script(src, engine_api)

collider1 = Collider()
collider1.set_shape(Box(10, 10, 10))

collider2 = Collider()
collider2.set_shape(Box(2, 2, 2))

transform = np.identity(4)
transform[3][0] = 0.5
collider2.set_transform(transform)


mesh_renderer = MeshRenderer("../../assets/models/Trollboyobj.obj")

clickable = Clickable()


node1 = Node("Node1", transform  = np.identity(4))

node1.add_component(script1)
node1.add_component(collider1)
node1.add_component(mesh_renderer)
node1.add_component(clickable)

node2 = Node("Node2", transform = np.identity(4))
node2.add_component(collider2)

camera = Camera()
eye = [15.0, 0.0, 0.0]
camera.set_eye(eye)
camera.set_target([0.0, 0.0, 0.0])

node3 = Node("Camera", transform = np.identity(4))
node3.add_component(camera)

scene_graph.add_node(node1)
scene_graph.add_node(node2)
scene_graph.add_node(node3)

game_manager = GameManager()
game_manager.run()