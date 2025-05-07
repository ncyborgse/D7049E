import dearpygui.dearpygui as dpg
from editor.window.window import Window
from editor.element.button import Button
from editor.window.test_window import TestWindow
from editor.window.inspector_window import InspectorWindow
from editor.window.scene_graph_window import SceneGraphWindow


class MainWindow(Window):

    def __init__(self, name, width=1200, height=900):
        super().__init__(name, width, height)

    def draw_self(self):
        #with dpg.group(horizontal=True):
        dpg.add_text("Welcome to the Main Window!")
        dpg.add_button(label="Exit Program", callback=lambda: dpg.stop_dearpygui())
#        dpg.add_spacing(count=3)
        dpg.add_text("This is the main content area.")            


