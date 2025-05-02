from scene.component.component import Component
from lupa import LuaRuntime
from utilities.lua_proxy import LuaProxy
from core.component_registry import register_component


@register_component
class Script(Component):
    def __init__(self, name="Script"):
        super().__init__(name=name)
        self.source = None
        self.lua = LuaRuntime(unpack_returned_tuples=True)

        # Try to create a table to see if Lua is working

        self.globals = None

        # Set up environment for Lua

        self.environment = None
        self.event_callbacks = {}
        self.engine_api = {}  

        # Script context

        self.public_vars = None
        self.public_functions = None

    def subscribe(self, event_emitter):
        supported_events = ['onStart', 'onUpdate', 'onRender', 'onSpawn', 'onDestroy'] # Maybe load from file

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

    def on_runtime_init(self, scene_manager):
        # Add engine API to Lua environment
        engine_api = {
            "SceneManager" : {
                "load_scene" : scene_manager.load_scene,
                "get_current_scene" : scene_manager.get_current_scene,
                "get_scenes" : scene_manager.get_scenes,
            }
        }

        self.engine_api = engine_api

        # Read script file and subscribe to events

        public_vars = self.public_vars if self.public_vars else {}

        with (open(self.source, 'r')) as file:
            script = file.read()

            self.environment = self.create_environment()
        
            # Inject public variables into the environment

            if public_vars:
                for var_name, var_value in public_vars.items():
                    self.environment[var_name] = LuaProxy(var_value, self.lua)
        
            loader_func = self.lua.execute('''
                    return function(script_code, env)
                        local chunk, err = load(script_code, "script", "t", env)
                        return chunk, err
                    end
            ''')
            
            if not callable(loader_func):
                raise RuntimeError("Loader function is not callable.")

            chunk, err = loader_func(script, self.environment)
            if not chunk:
                raise RuntimeError(f"Failed to load script\n{err}")
            
            try:
                chunk()
            except Exception as e:
                raise RuntimeError(f"Error executing script: {e}")

            self.globals = self.environment


        

    def create_environment(self):
        env = self.lua.table()

        env["print"] = self.lua.globals()["print"]
        env["math"] = self.lua.globals()["math"]
        env["ipairs"] = self.lua.globals()["ipairs"]

        game_api = self.lua.table()

        for component_name, component in self.engine_api.items():

            # Expose the proxy object to Lua

            proxy = LuaProxy(component, self.lua)
            game_api[component_name] = proxy

        env["game"] = game_api

        return env

    def attach_script(self, source, public_vars=None):
        self.source = source
        self.public_vars = public_vars if public_vars else {}

    def run_function(self, func_name, *args):
        if self.globals and func_name in self.globals:
            func = self.globals[func_name]
            if callable(func):
                return func(*args)
            else:
                raise TypeError(f"Function '{func_name}' is not callable.")
        else:
            raise RuntimeError(f"Function '{func_name}' not found in script context.")
        
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "source": self.source,
            "public_vars": self.public_vars,
        })
        return base

    @classmethod
    def from_dict(self, data):
        name = data.get("name", "Script")
        source = data.get("source")
        public_vars = data.get("public_vars", {})
        script = Script(name=name)
        script.attach_script(source, public_vars)
        return script
