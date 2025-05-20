import dearpygui.dearpygui as dpg
from editor.window.window import Window
from editor.element.component_element import ComponentElement
from editor.element.add_component_element import AddComponentElement

class InspectorWindow(Window):
    def __init__(self, name, width=400, height=600):
        super().__init__(name, width, height)
        self.selected_node = None  # Placeholder for the active node


    def load_node(self, node):
        self.selected_node = node
        self.refresh_inspector()


    def refresh_inspector(self, node=None):
        if node is not None:
            self.selected_node = node

        if self.selected_node:
            for component in self.selected_node.get_components():
                self.add_child(ComponentElement(component))

            self.add_child(AddComponentElement(self.selected_node))

        if self.is_opened:
            self.unload()
            self.load()


    def draw_self(self, parent=None):
        dpg.add_text("Inspector")
        dpg.add_separator()

        #if self.selected_node:
        #    dpg.add_text(f"Selected: {self.selected_node.get_name()}", parent=self.name)
        #else:
        #    dpg.add_text("No node selected", parent=self.name)