# path stuff
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import dearpygui.dearpygui as dpg
from editor.display_manager import DisplayManager
from editor.window.main_window import MainWindow

# Create an instance of InterfaceManager   
manager = DisplayManager()
# Create a MainWindow instance
main_window = MainWindow("Main Window")

# Add the window to the manager
manager.add_window(main_window)

manager.load_context()

manager.load_window("Main Window")

manager.load_gui()