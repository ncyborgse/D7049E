from scene.components.component import Component
from lupa import LuaRuntime

class Script(Component):
    def __init__(self):
        super().__init__(name="Script")
        self.source = None
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.globals = None
        self.event_callbacks = {}

    def subscribe(self, event_emitter):
        supported_events = ['onStart', 'onUpdate', 'onRender', 'onDestroy'] # Maybe load from file
        
        # Check if context is set
        if not self.globals:
            raise RuntimeError("Script context is not set. Please attach a script first.")

        for event in supported_events:
            callback = self.globals[event]
            if callback:
                if callable(callback):
                    event_emitter.on(event, callback)
                else:
                    raise TypeError(f"Event '{event}' is not callable.")

    def attachScript(self, source):
        self.source = source
        # Read script file and subscribe to events
        with (open(self.source, 'r')) as file:
            script = file.read()


            wrapped_script = f"""
            function __script_loader__()
            {script}
            end
            """

            self.lua.execute(wrapped_script)
            self.globals = self.lua.globals()

            loader = self.globals["__script_loader__"]
            if callable(loader):
                loader()
                del self.globals["__script_loader__"]  # Optional cleanup
            else:
                raise RuntimeError("Script does not contain a valid __script_loader__ function")