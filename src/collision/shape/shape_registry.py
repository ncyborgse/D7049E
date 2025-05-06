shape_registry = {}

def register_shape(component_class):

    shape_registry[component_class.__name__] = component_class
    return component_class