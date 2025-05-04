from pathlib import Path
import json



class ConfigManager:
    def __init__(self):
        self.config_src = Path(__file__).parent.parent.parent / "assets" / "config" / "config.json"
        # If the config file does not exist, create it with default values
        if not self.config_src.exists():
            config = {
                "projects_path": str(Path.home() / "projects"),
            }
            with open(self.config_src, 'w') as file:
                json.dump(config, file, indent=4)

    def get_config(self):
        with open(self.config_src, 'r') as file:
            config = json.load(file)
        return config

    def save_config(self):
        with open(self.config_src, 'w') as file:
            json.dump(self.config, file, indent=4)

    def set_projects_path(self, project_path: Path):
        with open(self.config_src, 'r') as file:
            config = json.load(file)
            config["projects_path"] = str(project_path)
        with open(self.config_src, 'w') as file:
            json.dump(config, file, indent=4)

    
