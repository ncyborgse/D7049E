from core.scene_manager import SceneManager
from core.state_manager import StateManager
from editor.display_manager import DisplayManager
from editor.window.project_selection_window import ProjectSelectionWindow
import sys


def main():
    if __name__ == "__main__":
        # Start the editor
        scene_manager = SceneManager()
        state_manager = StateManager()

        state_manager.set_scene_manager(scene_manager)

        # Create an instance of InterfaceManager   
        manager = DisplayManager()

        main_window = ProjectSelectionWindow("Project Selection Window", state_manager)

        # Add the window to the manager
        manager.add_window(main_window)

        manager.load_context()

        manager.load_window("Project Selection Window")

        manager.load_gui()


if sys.version_info[:3] != (3, 11, 0):
    sys.exit("This project requires Python 3.11.0")
