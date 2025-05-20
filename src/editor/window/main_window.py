import dearpygui.dearpygui as dpg
from editor.window.window import Window


class MainWindow(Window):

    def __init__(self, name, state_manager, width=1200, height=900):
        super().__init__(name, width, height)
        self.state_manager = state_manager

    def draw_self(self, parent=None):
        # with dpg.group(horizontal=True):
        dpg.add_text("Welcome to the Main Window!")
        dpg.add_button(label="Exit Program", callback=lambda: self.exit_program())
        dpg.add_button(label="Run Program", callback=lambda: self.run_program())
        dpg.add_button(label="Save Project", callback=lambda: self.state_manager.save_project())
        # dpg.add_spacing(count=3)
        dpg.add_text("This is the main content area.")            

    def exit_program(self):
        print("Exiting program... ")
        self.state_manager.save_project()
        dpg.stop_dearpygui()

    def run_program():
        pass
