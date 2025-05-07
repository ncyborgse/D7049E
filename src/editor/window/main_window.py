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
        dpg.add_text("Welcome to the Main Window!")
        dpg.add_button(label="Close", callback=lambda: self.unload())
        dpg.add_button(label="Exit Program", callback=lambda: dpg.stop_dearpygui())
        #button1 = Button("Button1", "Click Me!", width=100, height=30, callback=lambda: print("Button 1 clicked!"))
        #button2 = Button("Button2", "Close", width=100, height=30, callback=lambda: self.unload())
        #self.add_child(button1)
        #self.add_child(button2)

        # Inspector Window
        inspector_window = InspectorWindow("Inspector")
        self.add_child(inspector_window)
        #inspector_window.load()
        #dpg.set_item_pos("Inspector", [self.width - inspector_window.width, 0])

        # Scene Graph window
        scene_graph_window = SceneGraphWindow("Scene Graph", inspector_window=inspector_window)
        self.add_child(scene_graph_window)


