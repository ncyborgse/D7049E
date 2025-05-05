import dearpygui as dpg
from editor.window.window import Window
from editor.element.component_element import SceneGraphElement, AddSceneGraphElement


class SceneGraphWindow(Window):
    def __init__(self, name, width=400, height=600):
        super().__init__(name, width, height)
        self.selected_scene_graph = None  # Placeholder for the active scene graph

    def load_scene_graph(self, scene_graph):
        self.selected_scene_graph = scene_graph
        self.refresh_scene_graph_window()

    def refresh_scene_graph_window(self):
        self.children.clear()

        if self.selected_scene_graph:
            for node in self.selected_scene_graph.get_root().get_children():
                self.add_child(SceneGraphElement(node))
            
            self.add_child(AddSceneGraphElement(self.selected_scene_graph))

        if self.is_opened:
            self.unload()
            self.load()
    
    def draw_self(self):
        with dpg.window(label=self.name, tag=self.name, width=self.width, height=self.height):
            dpg.add_text("Scene Graph")
            dpg.add_separator()
