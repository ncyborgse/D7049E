from core.game_manager import GameManager
from core.global_scene_manager import scene_manager
from core.config_manager import ConfigManager
import os
from scene.objects.node_builder import NodeBuilder
from core.state_manager import StateManager
import sys
import yappi


if __name__ == "__main__":
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        raise ValueError("Please provide a project name as a command line argument.")

    
    # Initialize the state manager and game manager
    state_manager = StateManager()
    state_manager.set_scene_manager(scene_manager)
    game_manager = GameManager()

    state_manager.load_project(project_name)
    scene_manager.set_current_scene(scene_manager.get_scenes()[0])

    yappi.start()

    game_manager.run()

    yappi.stop()

    yappi.get_func_stats().print_all()

    yappi.get_thread_stats().print_all()

