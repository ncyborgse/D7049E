from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg
from editor.element.display_element import DisplayElement

class Window(ABC):
    def __init__(self, name, width=1200, height=600):
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

    def load(self, parent=None):
        print("debug | Window/load()")
        if not self.is_opened:
            with dpg.window(label=self.name, tag=self.name, width=self.width, height=self.height):
                self.draw_self(parent)
            for child in self.children:
                if isinstance(child, Window):
                    with dpg.child_window(width=child.width, height=child.height, tag=child.name, parent=self.name):
                        child.load()
                else:
                    with dpg.group(tag=child.name, parent=self.name):
                        child.load()
        else:
            print(f"Window '{self.name}' is already loaded.")

    def unload(self):
        if self.is_opened:
            dpg.hide_item(self.name)
            dpg.delete_item(self.name)
            self.is_opened = False
        else:
            print(f"Window '{self.name}' is not loaded.")
    
    def is_open(self):
        return self.is_opened


    @abstractmethod
    def draw_self(self, parent=None):
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
