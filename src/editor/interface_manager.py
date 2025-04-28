import dearpygui.dearpygui as dpg


class InterfaceManager:
    def __init__(self):
        self.windows = []

    def load_context(self):
        dpg.create_context()
        dpg.create_viewport(title='4X Engine', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()


    def load_gui(self):
        dpg.start_dearpygui()
        dpg.destroy_context()

    def add_window(self, window):
        self.windows.append(window)

    def remove_window(self, window_name):
        for window in self.windows:
            if window.name == window_name:
                self.windows.remove(window)
                break
        else:
            print(f"Window '{window_name}' not found.")

    def load_window(self, window_name):
        for window in self.windows:
            if window.name == window_name:
                with dpg.window(label=window.name, tag=window.name, width=window.width, height=window.height):
                    window.load()
                break
        else:
            print(f"Window '{window_name}' not found.")
    
    def unload_window(self, window_name):
        for window in self.windows:
            if window.name == window_name:
                window.unload()
                break
        else:
            print(f"Window '{window_name}' not found.")

    def is_open(self, window_name):
        for window in self.windows:
            if window.name == window_name:
                return window.is_open()
        return False