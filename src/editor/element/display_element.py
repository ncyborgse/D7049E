from abc import ABC, abstractmethod
import dearpygui.dearpygui as dpg


class DisplayElement(ABC):
    def __init__(self, name, width=800, height=600):
        self.width = width
        self.height = height
        self.name = name
        self.children = []


    def add_child(self, child):
        if isinstance(child, DisplayElement):
            self.children.append(child)
        else:
            raise TypeError("Child must be an instance of a display element.")

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
        else:
            raise ValueError("Child not found in children list.")

    @abstractmethod
    def draw_self(self):
        pass

    def load(self):
        self.draw_self()
        for child in self.children:
            with dpg.child_window(width=self.width, height=self.height, tag=child.name):
                child.load()
        