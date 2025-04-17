import dearpygui.dearpygui as dpg
from interface.interface_manager import InterfaceManager
from interface.windows.main_window import MainWindow

# Create an instance of InterfaceManager   
manager = InterfaceManager()
# Create a MainWindow instance
main_window = MainWindow("Main Window")
# Add the window to the manager
manager.add_window(main_window)

manager.load_context()

manager.load_window("Main Window")

manager.load_gui()



