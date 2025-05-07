import pathlib
from scene.objects.node_builder import NodeBuilder
from scene.component.components.script import Script
from scene.scene_graph import SceneGraph
from core.scene_manager import SceneManager
from scene.objects.node import Node
import numpy as np
from pyee import EventEmitter


def create_prefabs():

    scene_manager = SceneManager()

    scene_graph = SceneGraph(name="Scene1")

    scene_manager.add_scene(scene_graph)
    scene_manager.load_scene("Scene1")



    emitter = EventEmitter()



    src = pathlib.Path(__file__).parent.parent / "assets" / "prefabs"
    
    # Attach a script to a node
    script1 = Script("Script1")
    scriptSrc = "src/test/testScript.lua"

    script1.attach_script(scriptSrc)
    script1.subscribe(emitter)

    node1 = Node("Node1", transform = np.identity(4), parent=None)
    node1.add_component(script1)
    scene_graph.add_node(node1)

    node_builder = NodeBuilder(src)
    node_builder.save_prefab("Prefab1", node1)

    emitter.emit("onStart")


def load_and_run():
    src = pathlib.Path(__file__).parent.parent / "assets" / "prefabs"
    node_builder = NodeBuilder(src)

    scene_manager = SceneManager()
    scene_graph = SceneGraph(name="Scene1")
    scene_manager.add_scene(scene_graph)
    scene_manager.load_scene("Scene1")

    event_emitter = EventEmitter()

    node = node_builder.build("Prefab1")


    for component in node.get_components():
        component.on_runtime_init(scene_manager)
        component.subscribe(event_emitter)
    
    event_emitter.emit("onStart")


load_and_run()

    
    