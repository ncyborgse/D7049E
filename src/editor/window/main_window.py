import subprocess
import sys
import dearpygui.dearpygui as dpg
from pathlib import Path
from editor.window.window import Window


class MainWindow(Window):

    def __init__(self, name, state_manager, width=1200, height=900):
        super().__init__(name, width, height)
        self.state_manager = state_manager

    def draw_self(self, parent=None):
        dpg.add_text("Welcome to the Main Window!")
        dpg.add_button(label="Exit Program", callback=lambda: self.exit_program())
        dpg.add_button(label="Run Program", callback=lambda: self.run_program())
        dpg.add_button(label="Save Project", callback=lambda: self.state_manager.save_project())
        dpg.add_text("This is the main content area.")

    def exit_program(self):
        print("Exiting program...")
        self.state_manager.save_project()
        dpg.stop_dearpygui()

    def run_program(self):
        print("Running program...")

        if self.state_manager.get_scene_manager():
            project_name = self.state_manager.get_scene_manager().get_current_proj()
        
            file = Path(__file__).parent.parent.parent / "core" / "run_game.py"
            if not file.exists():
                raise FileNotFoundError(f"File {file} does not exist.")

            subprocess.Popen([sys.executable, file, project_name])

        else:
            print("SceneManager doesn't exist")