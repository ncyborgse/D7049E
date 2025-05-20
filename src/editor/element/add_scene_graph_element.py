import dearpygui.dearpygui as dpg
from editor.element.display_element import DisplayElement
from core.global_scene_manager import scene_manager
from scene.objects.node_builder import NodeBuilder
from editor.element.scene_graph_element import SceneGraphElement


class AddSceneGraphElement(DisplayElement):
    def __init__(self, inspector_callback=None, refresh_callback=None, width=800, height=30):
        super().__init__("AddNode", width, height)
        self.node_builder = NodeBuilder("assets/prefabs")
        self.inspector_callback = inspector_callback 
        self.refresh_callback = refresh_callback
        self.scene_manager = scene_manager
        self.selected_prefab = None

    def draw_self(self):
        dpg.add_text("Add Node to Scene Graph")
        prefab_names = self.node_builder.get_prefab_names()
        combo_tag = f"{self.name}_combo"
        dpg.add_combo(prefab_names, label="Select Prefab", callback=self._on_prefab_selected, tag=combo_tag)
        dpg.add_button(label="Add Node", callback=self._on_add_node)

    def _on_prefab_selected(self, sender, app_data, user_tag):
        self.selected_prefab = app_data
        print(f"Prefab selected: {self.selected_prefab}")


    def _on_add_node(self, sender, app_data, user_data=None):
        if hasattr(self, 'selected_prefab') and self.selected_prefab:
            try:
                print("\n", "debug | AddSceneGraphElement/_on_add_node begining")

                node = self.node_builder.build(self.selected_prefab)
                print("debug | AddSceneGraphElement/_on_add_node  after build()")

                scene_graph = self.scene_manager.get_current_scene()
                print("debug | AddSceneGraphElement/_on_add_node  adfter get_current_scene()")

                if scene_graph and scene_graph.get_root():
                    print("debug | AddSceneGraphElement/_on_add_node  in if statement")

                    scene_graph.get_root().add_child(node)
                    print(f"Added node '{node.get_name()}' to scene graph")
                    print("SceneGraph's children: ", scene_graph.get_root().get_children(), "\n")

                    if self.refresh_callback:
                        self.refresh_callback()

                    if self.inspector_callback:
                        self.inspector_callback()

                else:
                    print("No valid scene graph or root node found.")
            except Exception as e:
                print(f"Error adding node: {e}")
        else:
            print("No prefab selected!")



'''
def _on_add_node(self, sender, app_data, user_data=None):
        if self.selected_prefab:
            print("debug | AddSceneGraphElement (in _on_add_node) Adding a node!")
            node = self.node_builder.build(self.selected_prefab)
            scene_graph = self.scene_manager.get_current_scene()
            scene_graph.get_root().add_child(node)

            print(f"Added node '{node.get_name()}' to scene graph")

            if self.refresh_callback:
                self.refresh_callback()  # Refresh scene graph window

            if self.inspector_callback:
                self.inspector_callback(node)  # Update inspector with new node
        else:
            print("No prefab selected!")
'''