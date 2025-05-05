import dearpygui as dpg
from editor.element.display_element import DisplayElement
from utilities.component_loader import get_available_components

class AddComponentElement(DisplayElement):
    def __init__(self, node, width=800, height=200):
        super().__init__("AddComponentElement", width, height)
        self.node = node
        self.available_components = get_available_components()  # Placeholder for available components
        self.dropdown_tag = f"{self.name}_dropdown"
        self.button_tag = f"{self.name}_button"

    def draw_self(self):
        dpg.add_text("Add Component")
        dpg.add_combo(list(self.available_components.keys()), tag=self.dropdown_tag, width=200)
        dpg.add_button(label="Add", tag=self.button_tag, callback=self._on_add_clicked, used_data=self)

    def _on_add_clicked(self, sender, app_data, user_data):
        selected_component = dpg.get_value(self.dropdown_tag)
        component_cls = self.available_components.get(selected_component)
        if component_cls:
            new_component = component_cls(name=selected_component)
            self.node.add_component(new_component)
            print(f"Added {selected_component} to {self.node.name}")
        else:
            print(f"Component {selected_component} not found in available components.")