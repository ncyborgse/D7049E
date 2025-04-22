'''
name

invoke(Node)
subscribe(EventEmitter)
unsubscribe(EventEmitter)
attach(Node)
'''
class Component:
    def __init__(self, name):
        self.name = name

    def invoke(self, node):
        pass

    def subscribe(self, event_emitter):
        # Subscribe to the event
        pass

    def unsubscribe(self, event_emitter):
        # Unsubscribe from the event
        pass

    def attach(self, node):
        node.add_component(self)