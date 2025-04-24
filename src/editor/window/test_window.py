import dearpygui.dearpygui as dpg
from editor.window.window import Window
from editor.element.button import Button


class TestWindow(Window):

    def __init__(self, name, width=300, height=200):
        super().__init__(name, width, height)

    def draw_self(self):
        dpg.add_text("This is a smaller test window.")
        dpg.add_button(label="Close", callback=lambda: self.unload())