import dearpygui.dearpygui as dpg
from editor.element.display_element import DisplayElement

class SceneGraphElement(DisplayElement):
    def __init__(self, node, inspector_callback=None, refresh_callback=None, width=800, height=30):
        super().__init__(node.get_name(), width, height)
        self.node = node
        self.inspector_callback = inspector_callback #refresh inspector window
        self.refresh_callback = refresh_callback #refresh sceneGraph window
        self.selected = False

    def draw_self(self):
        with dpg.tree_node(label=self.node.get_name(), default_open=True):
            dpg.add_button(label="Select", callback=self._on_select)
            dpg.add_button(label="Delete", callback=self._on_delete, user_data=self.node)

            for child_node in self.node.get_children():
                child_element = SceneGraphElement(
                    child_node,
                    inspector_callback=self.inspector_callback,
                    refresh_callback=self.refresh_callback
                )
                child_element.draw_self()

    def _on_select(self, sender, app_data, user_data=None):
        print(f"Selected node: {self.node.get_name()}")
        if self.inspector_callback:
            self.inspector_callback(self.node)

    def _on_delete(self, sender, app_data, user_data=None):
        node = user_data
        parent = node.get_parent()
        if parent:
            parent.remove_child(node)
            print(f"Deleted node '{node.get_name()}' from parent '{parent.get_name()}'")

        if self.refresh_callback:
            self.refresh_callback()
