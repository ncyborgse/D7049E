import dearpygui.dearpygui as dpg
from editor.window.window import Window
from editor.element.button import Button
from editor.window.test_window import TestWindow


class MainWindow(Window):

    def __init__(self, name, width=1200, height=900):
        super().__init__(name, width, height)

    def draw_self(self):
        dpg.add_text("Welcome to the Main Window!")
        dpg.add_button(label="Close", callback=lambda: self.unload())
        button1 = Button("Button1", "Click Me!", width=100, height=30, callback=lambda: print("Button 1 clicked!"))
        button2 = Button("Button2", "Close", width=100, height=30, callback=lambda: self.unload())
        self.add_child(button1)
        self.add_child(button2)
        self.add_child(TestWindow("Test Window", 300, 200))
