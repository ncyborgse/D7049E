import os, importlib, inspect
from scene.component.component import Component
from scene.component.components import __path__ as components_path

def get_available_components():
    component_classes = {}
    directory = components_path[0]

    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"scene.component.components.{filename[:-3]}"
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Component) and obj is not Component:
                    component_classes[name] = obj

    return component_classes