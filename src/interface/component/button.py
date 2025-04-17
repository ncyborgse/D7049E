import dearpygui.dearpygui as dpg
from interface.component.interface_component import InterfaceComponent

class Button(InterfaceComponent):
    def __init__(self, name, label, width=100, height=30, callback=None):
        super().__init__(name, width, height)
        self.label = label
        self.callback = callback

    def draw_self(self):
        dpg.add_button(label=self.label, width=self.width, height=self.height, callback=self.callback)
        dpg.set_item_label(self.name, self.label)