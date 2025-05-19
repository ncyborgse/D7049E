from core.config_manager import ConfigManager
from core.scene_manager import SceneManager
from scene.objects.node_builder import NodeBuilder
from scene.scene_graph import SceneGraph
#from pathlib import Path
import os


class StateManager:
    def __init__(self):
        self.current_project = None
        self.config_manager = ConfigManager()

        # Identify the source directory for the users projects

        # Config manager?

    def set_scene_manager(self, scene_manager: SceneManager):
        self.scene_manager = scene_manager

    def new_project(self, project_name):
        print("debug | state manager/new project\n")
        # Get the project path from the config manager
        project_path = self.config_manager.get_config()["projects_path"]
        
        # Create the project directory if it doesn't exist

        project_dir = project_path + "/" + project_name
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        else:
            raise FileExistsError(f"Project '{project_name}' already exists.")
        
        new_scene = SceneGraph(name=f"{project_name}_scene")
        self.scene_manager.add_scene(new_scene)
        self.scene_manager.load_scene(new_scene.get_name())
        # self.scene_manager.set_current_scene(new_scene) # already exists in load_scene

    def save_project(self):
        if self.current_project is None:
            raise ValueError("No project is currently loaded.")
        
        if self.scene_manager is None:
            raise ValueError("No scene manager is set.")
        
        # Save the current scene to the project directory
        project_path = self.config_manager.get_config()["projects_path"]
        project_dir = project_path + "/" + self.current_project
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"Project '{self.current_project}' does not exist.")
        
        # Serialize the current scene graph 
        scenes = self.scene_manager.get_scenes()
        for scene in scenes:
            root = scene.get_root()
            scene_name = scene.get_name()
            self.node_builder.save_prefab(scene_name, root)
            

    def load_project(self, project_name):
        print("debug | state manager/load project\n")

        if self.scene_manager is None:
            raise ValueError("No scene manager is set.")
        
        # Load the project directory and its scenes
        project_path = self.config_manager.get_config()["projects_path"]
        project_dir = project_path + "/" + project_name
        if not os.path.exists(project_dir):
            raise FileNotFoundError(f"Project '{self.current_project}' does not exist.")
        
        # Create a NodeBuilder instance for the project directory
        self.node_builder = NodeBuilder(project_dir)

        # Load the scenes from the project directory

        for scene_name in os.listdir(project_dir):
            if scene_name.endswith(".json"):
                scene_path = os.path.join(project_dir, scene_name)
                print("Building scene:", scene_name[:-5])
                root = self.node_builder.build(scene_name[:-5])
                scene = SceneGraph(node=root, name=scene_name[:-5])
                self.scene_manager.add_scene(scene)

        self.current_project = project_name

        # Load the first scene by default
        
        if self.scene_manager.get_scenes():
            self.scene_manager.load_scene(self.scene_manager.get_scenes()[0].get_name())


    def list_projects(self):
        
        # List all projects in the project names in directory
        project_path = self.config_manager.get_config()["projects_path"]
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Project directory '{project_path}' does not exist.")
        
        projects = [d for d in os.listdir(project_path) if os.path.isdir(os.path.join(project_path, d))]
        return projects