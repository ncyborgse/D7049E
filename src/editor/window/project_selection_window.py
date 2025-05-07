from editor.window.window import Window
from scene.objects.node_builder import NodeBuilder
from core.config_manager import ConfigManager
import dearpygui.dearpygui as dpg
import os
from editor.window.main_window import MainWindow

class ProjectSelectionWindow(Window):
    def __init__(self, name, state_manager, width=400, height=300):
        super().__init__(name, width, height)
        self.config_manager = ConfigManager()
        self.state_manager = state_manager

    def draw_self(self):
        dpg.add_text("Select a project to load:")
        dpg.add_separator()
        
        project_src = self.config_manager.get_config()["projects_path"]

        # Get a list of all project folders in the projects directory
        project_folders = [f for f in os.listdir(project_src) if os.path.isdir(os.path.join(project_src, f))]
        
        for project in project_folders:
            # Create a button for each project folder
            dpg.add_button(label=project, callback= lambda: self.load_project(project))  # Load the project when clicked

        dpg.add_button(label="Close", callback=self.unload)  # Close button to unload the window
        
    def load_project(self, project_name):
        # Load the project using the state manager
        print(f"Loading project: {project_name}")
        self.state_manager.load_project(project_name)
        
        # Unload the project selection window after loading the project and load the main window
        main_window = MainWindow("main")
        self.unload()
        

        # Main window needs to be loaded from the display manager and be root there
        main_window.load()
        main_window.draw_self()

