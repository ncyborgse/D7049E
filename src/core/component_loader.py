import importlib
import pathlib
import os

def load_components():

    components_src = pathlib.Path(__file__).parent.parent / "scene" / "component" / "components"
    for file in os.listdir(components_src):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"scene.component.components.{file[:-3]}"
            importlib.import_module(module_name)