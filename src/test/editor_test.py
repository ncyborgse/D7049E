# path stuff
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import dearpygui.dearpygui as dpg
from core.scene_manager import SceneManager
from core.state_manager import StateManager
from editor.display_manager import DisplayManager
from editor.window.main_window import MainWindow
from editor.window.inspector_window import InspectorWindow
from editor.window.scene_graph_window import SceneGraphWindow
from editor.window.project_selection_window import ProjectSelectionWindow

scene_manager = SceneManager()
state_manager = StateManager()
state_manager.set_scene_manager(scene_manager)
display_manager = DisplayManager()

def on_project_loaded():
    main_window = MainWindow("Main")
    inspector = InspectorWindow("Inspector")
    scene_graph = SceneGraphWindow("Scene Graph", inspector_window=inspector)

    display_manager.add_window(main_window)
    display_manager.add_window(inspector)
    display_manager.add_window(scene_graph)

    display_manager.load_window("Main")
    display_manager.load_window("Scene Graph")
    display_manager.load_window("Inspector")

selection_window = ProjectSelectionWindow("Project Selection Window", state_manager, on_project_loaded)
display_manager.add_window(selection_window)

display_manager.load_context()
display_manager.load_window("Project Selection Window")
display_manager.load_gui()
