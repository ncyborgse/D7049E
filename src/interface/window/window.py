from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg
from interface.component.component import Component

class Window(ABC):
    def __init__(self, name, width=800, height=600):
        self.name = name
        self.width = width
        self.height = height
        self.is_opened = False
        self.components = []
    
    def add_component(self, component):
        if isinstance(component, Component):
            self.components.append(component)
        else:
            raise TypeError("Component must be an instance of Component.")

    def load(self):
        self.draw_self()
        for component in self.components:
            with dpg.child_window(width=component.width, height=component.height, tag=component.name, parent=self.name):
                component.draw()

    @abstractmethod
    def draw_self(self):
        pass

    def unload(self):
        if self.is_opened:
            dpg.hide_item(self.name)
            dpg.delete_item(self.name)
            self.is_opened = False
        else:
            print(f"Window '{self.name}' is not loaded.")
    
    def is_open(self):
        return self.is_opened