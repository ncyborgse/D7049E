import dearpygui as dpg
import numpy as np
from editor.element.display_element import DisplayElement

class ComponentElement(DisplayElement):
    def __init__(self, component, width=800, height=200):
        super().__init__(component.get_name(), width, height)
        self.component = component

    def draw_self(self):
        with dpg.child_window(border=True, width=self.width - 20, height=150):  # Add border and padding
        # Add component name
            dpg.add_text(self.component.get_name())
        
            dpg.add_input_text(
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
                elif isinstance(value, list):
                    dpg.add_input_text_multiline(
                        label=field,
                        default_value=str(value),
                        callback=self._update_field,
                        user_data=(self.component, field)
                    )
                elif isinstance(value, np.ndarray) and value.shape == (4, 4):
                    for row_index in range(4):
                        dpg.add_input_float4(
                            label=f"{field}[{row_index}]",
                            default_value=value[row_index].tolist(),
                            callback=self._update_matrix_row,
                            user_data=(self.component, field, row_index)
                        )
                else:
                    msg = f"Unsupported field type in component '{self.component.get_name()}': '{field}' ({type(value).__name__})"
                    print(msg)
                    dpg.add_text(msg)



    def _update_name(self, sender, app_data, user_data):
        user_data.name = app_data
        self.name = app_data

    def _update_field(self, sender, app_data, user_data):
        component, field = user_data
        setattr(component, field, app_data)

    def _update_matrix_row(self, sender, app_data, user_data):
        component, field, row_index = user_data
        matrix = getattr(component, field)
        matrix[row_index] = np.array(app_data)