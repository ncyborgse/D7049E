from scene.components.script import Script
from scene.scene_graph import SceneGraph
from scene.objects.node import Node
from pyee import EventEmitter


scene_graph = SceneGraph()

emitter = EventEmitter()

engine_api = {
    "SceneGraph" : {
        "get_root": scene_graph.get_root,
        "add_node": scene_graph.add_node,
        "move_node": scene_graph.move_node,
        "get_by_name_in": scene_graph.get_by_name_in,
    }
}


src = "src/test/testScript.lua"
script1 = Script("Script1", engine_api=engine_api)
script1.attach_script(src)
script1.subscribe(emitter)

node1 = Node("Node1", None)
node1.add_component(script1)
scene_graph.add_node(node1)

src2 = "src/test/testScript2.lua"
script2 = Script("Script2", engine_api=engine_api)
script2.attach_script(src2)
script2.subscribe(emitter)

node2 = Node("Node2", None)
node2.add_component(script2)
scene_graph.add_node(node2)

emitter.emit("onStart")