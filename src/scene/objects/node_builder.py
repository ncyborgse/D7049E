import os
import json
import pathlib

from scene.objects.node import Node


class NodeBuilder:
    def __init__(self, path):
        self.path = path

    def build(self, prefabName):
        prefab_path = os.path.join(self.path, f"{prefabName}.json")
        if not os.path.exists(prefab_path):
            raise FileNotFoundError(f"Prefab '{prefabName}' not found at {prefab_path}.")

        with open(prefab_path, 'r') as file:
            data = json.load(file)

        node = Node.from_dict(data)
        return node

    def get_prefab_names(self):
        prefab_names = []
        for file in os.listdir(self.path):
            if file.endswith(".json") and not file.startswith("__"):
                prefab_names.append(file[:-5])
        return prefab_names
    
    def save_prefab(self, prefabName, node):
        prefab_path = os.path.join(self.path, f"{prefabName}.json")
        data = node.to_dict()

        # Check if the directory exists, if not create it
        os.makedirs(self.path, exist_ok=True)

        # Check if the file already exists

        if os.path.exists(prefab_path):
            raise FileExistsError(f"Prefab '{prefabName}' already exists at {prefab_path}.")
        
        with open(prefab_path, 'w') as file:
            json.dump(data, file, indent=4)

        
