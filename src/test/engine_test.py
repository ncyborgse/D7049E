from scene.component.components.script import Script
from scene.scene_graph import SceneGraph
from core.scene_manager import SceneManager
from scene.objects.node import Node
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

node1 = Node("Node1", None)
node1.add_component(script1)
scene_graph.add_node(node1)

engine = Engine(scene_manager)
engine.run()


