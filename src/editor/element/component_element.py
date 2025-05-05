import dearpygui as dpg
from editor.element.display_element import DisplayElement

class ComponentElement(DisplayElement):
    def __init__(self, component, width=800, height=200):
        super().__init__(component.get_name(), width, height)
        self.component = component

    def draw_self(self):
        dpg.add_add_input(
            label="Name",
            default_value=self.component.get_name(),
            callback=self._update_name,
            user_data=self.component
        )

        for field, value in vars(self.component).items():
            if field == "name":
                continue

            if isinstance(value, int):
                dpg.add_int_input(
                    label=field,
                    default_value=value,
                    callback=self._update_field,
                    user_data=(self.component, field)
                )
            elif isinstance(value, float):
                dpg.add_float_input(
                    label=field,
                    default_value=value,
                    callback=self._update_field,
                    user_data=(self.component, field)
                )
            elif isinstance(value, str):
                dpg.add_input_text(
                    label=field,
                    default_value=value,
                    callback=self._update_field,
                    user_data=(self.component, field)
                )
            elif isinstance(value, bool):
                dpg.add_checkbox(
                    label=field,
                    default_value=value,
                    callback=self._update_field,
                    user_data=(self.component, field)
                )


    def _update_name(self, sender, app_data, user_data):
        user_data.name = app_data
        self.name = app_data

    def _update_field(self, sender, app_data, user_data):
        component, field = user_data
        setattr(component, field, app_data)
