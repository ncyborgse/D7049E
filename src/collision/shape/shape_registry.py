import os
import importlib
from pathlib import Path

shape_registry = {}

def register_shape(component_class):
    shape_registry[component_class.__name__] = component_class
    return component_class

def load_shapes():
    project_root = Path(__file__).parents[3]
    component_folder = project_root / "src" / "collision" / "shape" / "shapes"

    for file in os.listdir(component_folder):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"{component_folder}.{file[:-3]}"
            importlib.import_module("collision.shape.shapes." + file[:-3])


load_shapes()