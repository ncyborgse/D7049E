# path stuff
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from core.state_manager import StateManager
from core.global_scene_manager import scene_manager
from editor.display_manager import DisplayManager
from editor.window.main_window import MainWindow
from editor.window.inspector_window import InspectorWindow
from editor.window.scene_graph_window import SceneGraphWindow
from editor.window.project_selection_window import ProjectSelectionWindow

def init_editor():
    state_manager = StateManager()
    state_manager.set_scene_manager(scene_manager)
    display_manager = DisplayManager()

    def on_project_loaded():
        print("debug | Start of on_project_loaded \n")
        main_window = MainWindow("Main", state_manager)
        inspector = InspectorWindow("Inspector")
        scene_graph_window = SceneGraphWindow("Scene Graph", inspector_window=inspector)

        display_manager.add_window(main_window)
        display_manager.add_window(inspector)
        display_manager.add_window(scene_graph_window)

        display_manager.load_window("Main")
        display_manager.load_window("Scene Graph")
        display_manager.load_window("Inspector")
        print("debug | End of on_project_loaded \n")

    selection_window = ProjectSelectionWindow("Project Selection Window", state_manager, on_project_loaded)
    display_manager.add_window(selection_window)

    display_manager.load_context()
    display_manager.load_window("Project Selection Window")
    display_manager.load_gui()

    

    print("debug | 1 SceneManager.get_current_scene(): ", scene_manager.get_current_scene())
