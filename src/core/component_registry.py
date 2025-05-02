component_registry = {}

def register_component(component_class):

    component_registry[component_class.__name__] = component_class
    return component_class