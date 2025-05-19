import dearpygui.dearpygui as dpg
from editor.window.window import Window
from editor.element.scene_graph_element import SceneGraphElement
from editor.element.add_scene_graph_element import AddSceneGraphElement
from core.global_scene_manager import scene_manager


class SceneGraphWindow(Window):
    def __init__(self, name, inspector_window, width=400, height=600):
        super().__init__(name, width, height)
        self.inspector_window = inspector_window
        self.selected_scene_graph = scene_manager.get_current_scene()
        print("debug | (in SceneGraphWindow) SceneManager.get_current_scene(): ", scene_manager.get_current_scene())
        print("SceneGraphWindow initialized with scene graph:", self.selected_scene_graph)

    def load_scene_graph(self, scene_graph):
        print("scene graph window/load scene graph\n")

        self.selected_scene_graph = scene_graph
        self.refresh_scene_graph_window()

    def refresh_scene_graph_window(self):
        self.children.clear()

        if self.selected_scene_graph:
            for node in self.selected_scene_graph.get_root().get_children():
                self.add_child(SceneGraphElement(
                    node, 
                    inspector_callback=self.inspector_window.load_node,
                    refresh_callback=self.refresh_scene_graph_window
                ))
            
            self.add_child(AddSceneGraphElement(
                inspector_callback=self.inspector_window.load_node,
                refresh_callback=self.refresh_scene_graph_window,
            ))

        if self.is_opened:
            self.unload()
            self.load()
    
    def draw_self(self):
        dpg.add_text("Scene Graph")
        dpg.add_separator()
