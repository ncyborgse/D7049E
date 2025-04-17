import dearpygui.dearpygui as dpg
from interface.interface_manager import InterfaceManager
from interface.window.main_window import MainWindow
from interface.component.button import Button
# Create an instance of InterfaceManager   
manager = InterfaceManager()
# Create a MainWindow instance
main_window = MainWindow("Main Window")

button1 = Button("Button1", "Click Me!", width=100, height=30, callback=lambda: print("Button 1 clicked!"))
button2 = Button("Button2", "Close", width=100, height=30, callback=lambda: main_window.unload())

# Add buttons to the main window

main_window.add_component(button1)
main_window.add_component(button2)
# Add the window to the manager
manager.add_window(main_window)

manager.load_context()

manager.load_window("Main Window")

manager.load_gui()



