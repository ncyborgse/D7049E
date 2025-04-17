from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg

class Window(ABC):
    def __init__(self, name, width=800, height=600):
        self.name = name
        self.width = width
        self.height = height
        self.is_opened = False

    @abstractmethod
    def load(self):
        pass

    def unload(self):
        if self.is_opened:
            print(f"Unloading window '{self.name}'.")
            # Here you would typically close the window using a GUI library.
            self.is_opened = False
        else:
            print(f"Window '{self.name}' is not loaded.")
    
    def is_open(self):
        return self.is_opened