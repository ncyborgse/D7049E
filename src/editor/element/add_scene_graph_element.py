import dearpygui.dearpygui as dpg
from editor.element.display_element import DisplayElement

class AddSceneGraphElement(DisplayElement):
    def __ini__(self, node, inspector_callback=None, width=800, height=30):
        super().__init__(node.get_name(), width, height)
        self.node = node
        self.inspector_callback = inspector_callback 
        self.selected = False

    def draw_self(self):
        return super().draw_self()