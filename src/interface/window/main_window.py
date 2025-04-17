import dearpygui.dearpygui as dpg
from interface.window.window import Window
from interface.component.button import Button


class MainWindow(Window):

    def __init__(self, name, width=800, height=600):
        super().__init__(name, width, height)

    def draw_self(self):
        if not self.is_opened:
            with dpg.window(label=self.name, tag=self.name, width=self.width, height=self.height):
                dpg.add_text("Welcome to the Main Window!")
                dpg.add_button(label="Close", callback=lambda: self.unload())
                button1 = Button("Button1", "Click Me!", width=100, height=30, callback=lambda: print("Button 1 clicked!"))
                button2 = Button("Button2", "Close", width=100, height=30, callback=lambda: self.unload())
                self.add_component(button1)
                self.add_component(button2)
            dpg.show_item(self.name)
            print("Main window loaded.")
        else:
            print(f"Window '{self.name}' is already loaded.")