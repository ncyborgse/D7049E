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
        print("debug | (in SceneGraphWindow) SceneManager.get_current_scene(): ", scene_manager.get_current_scene(), "\n")
        print("SceneGraphWindow initialized with scene graph:", self.selected_scene_graph, "\n")
        self.set_root_node()
        self.children = []


    # function to create a SceneGraphElement for the root node
    def set_root_node(self):
        print("debug | scene graph window/set root node\n")
        scene_graph_root = self.selected_scene_graph.get_root()
        self.scene_graph_root_element = SceneGraphElement(scene_graph_root, self.inspector_window.refresh_inspector, self.refresh_scene_graph_window)


    def load_scene_graph(self, scene_graph):
        print("debug | scene graph window/load scene graph\n")

        self.selected_scene_graph = scene_graph
        self.set_root_node()
        self.refresh_scene_graph_window()


    def refresh_scene_graph_window(self):
        print("debug | scene graph window/refresh scene graph\n")
        self.children.clear()

        if self.selected_scene_graph:
            for node in self.selected_scene_graph.get_root().get_children():
                print("debug | Node: ", node)
                self.add_child(
                    SceneGraphElement(
                        node, 
                        inspector_callback=self.inspector_window.refresh_inspector(node),
                        refresh_callback=self.refresh_scene_graph_window
                    )
                )

            self.add_child(AddSceneGraphElement(
                inspector_callback=self.inspector_window.refresh_inspector,
                refresh_callback=self.refresh_scene_graph_window
            ))


        if self.is_opened:
            print("debug | self.is_opened, before unload()")
            self.unload()
            print("debug | after unload(), but before load()")
            self.load(self.get_parent())
            print("debug | after load()")


    def draw_self(self, parent=None):
        # These are now added inside the group/window created in load() using self.name as the tag
        dpg.add_text("Scene Graph", parent=self.name)
        dpg.add_separator(parent=self.name)

        with dpg.group(horizontal=True, parent=self.name):
            #dpg.add_button(label="Refresh", callback=self.refresh_scene_graph_window)
            # Fixed line
            dpg.add_button(label="Refresh", callback=lambda: self.refresh_scene_graph_window())

        dpg.add_separator(parent=self.name)

        # Draw the root scene graph element if it exists
        if self.scene_graph_root_element:
            self.scene_graph_root_element.draw_self()



'''
    def draw_self(self, parent=None):
        #with parent as window:
        #with dpg.window(tag=self.name):

        print("debug | SceneGraphWindow/draw_self, before dpg.add_text")
        #dpg.set_parent(parent)
        dpg.add_text("Scene Graph", parent=self.get_parent())
        print("debug | SceneGraphWindow/draw_self, after dpg.add_text")

        dpg.add_separator()
        #with dpg.group(horizontal=True):
        dpg.add_button(label="Refresh", callback=self.refresh_scene_graph_window())
        dpg.add_separator()
        self.scene_graph_root_element.draw_self()
'''