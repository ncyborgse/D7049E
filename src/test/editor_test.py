# path stuff
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import dearpygui.dearpygui as dpg
from editor.display_manager import DisplayManager
from editor.window.project_selection_window import ProjectSelectionWindow
from core.scene_manager import SceneManager
from core.state_manager import StateManager


scene_manager = SceneManager()
state_manager = StateManager()
state_manager.set_scene_manager(scene_manager)

# Create an instance of InterfaceManager   
manager = DisplayManager()
# Create a MainWindow instance
main_window = ProjectSelectionWindow("Project Selection Window", state_manager)

# Add the window to the manager
manager.add_window(main_window)

manager.load_context()

manager.load_window("Project Selection Window")

manager.load_gui()
