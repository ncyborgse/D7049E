from editor.window.window import Window
#from scene.objects.node_builder import NodeBuilder
from core.config_manager import ConfigManager
import dearpygui.dearpygui as dpg
import os
#from editor.window.main_window import MainWindow

class ProjectSelectionWindow(Window):
    def __init__(self, name, state_manager, on_project_loaded, width=1200, height=800):
        super().__init__(name, width, height)
        self.config_manager = ConfigManager()
        self.state_manager = state_manager
        self.on_project_loaded = on_project_loaded


    def draw_self(self):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Create New Project", callback=lambda: self.select_project_name()) 
            dpg.add_button(label="Exit Program", callback=lambda: dpg.stop_dearpygui())
        dpg.add_separator()
        
        dpg.add_text("Select a project to load:")
        project_src = self.config_manager.get_config()["projects_path"]

        # Get a list of all project folders in the projects directory
        project_folders = [f for f in os.listdir(project_src) if os.path.isdir(os.path.join(project_src, f))]
        
        for project in project_folders:
            # Create a button for each project folder
            dpg.add_button(label=project, callback= lambda: self.load_project(project))  # Load the project when clicked

        with dpg.window(label = "New Project", modal = True, show = False, id = "new_project_window", width = 300, height = 200):
            dpg.add_text("Enter new project name:")
            dpg.add_input_text(label="Project Name", tag="project_name_input")
            dpg.add_button(label="Create", callback=lambda: self.create_new_project(dpg.get_value("project_name_input")))
            #dpg.add_same_line()
            dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("new_project_window", show=False))


    def select_project_name(self):
        # Show the new project window when the button is clicked
        dpg.configure_item("new_project_window", show=True)

    def load_project(self, project_name):
        print("project selection window/load project\n")
        # Load the project using the state manager
        print(f"Loading project: {project_name}")
        self.state_manager.load_project(project_name)
        
        self.state_manager.save_project()
        self.unload()
        self.on_project_loaded()

    def create_new_project(self, project_name):
        print("project selection window/create new project\n")

        # Create a new project using the state manager
        self.state_manager.new_project(project_name)
        self.load_project(project_name)
