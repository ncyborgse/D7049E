## Must import all compontent to register them, do manually for now
import importlib
import os
import sys
from pathlib import Path


component_registry = {}


def load_components():
    project_root = Path(__file__).parents[2]
    component_folder = project_root / "src" / "scene" / "component" / "components"

    for file in os.listdir(component_folder):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"{component_folder}.{file[:-3]}"
            importlib.import_module("scene.component.components." + file[:-3])


def register_component(component_class):
    component_registry[component_class.__name__] = component_class
    return component_class

load_components()