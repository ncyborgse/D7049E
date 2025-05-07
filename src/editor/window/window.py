from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg
from editor.element.display_element import DisplayElement

class Window(ABC):
    def __init__(self, name, width=800, height=600):
        self.name = name
        self.width = width
        self.height = height
        self.is_opened = False
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        if isinstance(child, DisplayElement) or isinstance(child, Window):
            if child in self.children:
                raise ValueError("Component already exists in the window.")
            self.children.append(child)
            child.set_parent(self)
        else:
            raise TypeError("Component must be an instance of DisplayElement or Window.")

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    
    

    def load(self):
        if not self.is_opened:

            self.draw_self()
            self.is_opened = True
            for child in self.children:
                if isinstance(child, Window):
                    with dpg.child_window(width=child.width, height=child.height, tag=child.name, parent=self.name):
                        child.load()
                else:
                    with dpg.group(tag=child.name, parent=self.name):
                        child.load()
        else:
            print(f"Window '{self.name}' is already loaded.")

    @abstractmethod
    def draw_self(self):
        pass

    '''
    @abstractmethod
    def on_frame(self):
        pass

    def frame(self):
        if self.is_opened:
            for child in self.children:
                child.frame()
            self.on_frame()
        else:
            print(f"Window '{self.name}' is not loaded.")
    '''
    def unload(self):
        if self.is_opened:
            dpg.hide_item(self.name)
            dpg.delete_item(self.name)
            self.is_opened = False
        else:
            print(f"Window '{self.name}' is not loaded.")
    
    def is_open(self):
        return self.is_opened