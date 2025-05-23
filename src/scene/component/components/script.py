from scene.component.component import Component
from lupa import LuaRuntime
from utilities.lua_proxy import LuaProxy
from core.component_registry import register_component
from core.global_scene_manager import scene_manager
from core.config_manager import ConfigManager
import threading
from readerwriterlock import rwlock

@register_component
class Script(Component):
    def __init__(self, name="Script"):
        super().__init__(name=name)
        self.source = None
        self.lua = LuaRuntime(unpack_returned_tuples=True)

        # Try to create a table to see if Lua is working

        self.globals = None
        self.config_manager = ConfigManager()

        # Set up environment for Lua

        self.environment = None
        self.event_callbacks = {}
        self.engine_api = {}  

        # Script context

        self.public_vars = None
        self.public_functions = None

        self.lock = rwlock.RWLockFair()

    def subscribe(self, event_emitter):
        with self.lock.gen_wlock():
            supported_events = ['onStart', 'onUpdate', 'onRender', 'onSpawn', 'onDestroy', 'overlap', 'enter', 'exit', 'onClick', 'onDamageTaken', 'onHeal', 'onDeath', 'onKeyPress', 'onKeyHold', 'onKeyRelease', 'onAttack'] # Maybe load from file

            # Check if context is set
            if not self.globals:
                raise RuntimeError("Script context is not set. Please load a script first.")
            globs = self.globals

        for event in supported_events:
            callback = globs[event]
            if callable(callback):
                super().subscribe_to(event_emitter, event, callback)
        

    def create_environment(self):
        lua_globals = self.lua.globals()
        env = self.lua.table()

        # Copy standard Lua functions to the environment
        for name, func in lua_globals.items():
            if callable(func):
                env[name] = func

        blacklist = {
            "os": ["exit", "execute", "remove", "rename", "setlocale", "tmpname"],
            "io": ["open", "popen", "tmpfile", "type", "lines", "read", "write"],
            "_G": True,
            "dofile": True,
            "load": True,
            "loadfile": True,
            "require": True,
        }

        for key, value in blacklist.items():
            if value is True:
                env[key] = None
            elif isinstance(value, list):
                for func in value:
                    env[key][func] = None

        game_api = self.lua.table()

        for component_name, component in self.engine_api.items():

            # Expose the proxy object to Lua

            proxy = LuaProxy(component, self.lua)
            print(proxy.obj)
            game_api[component_name] = proxy

        env["game"] = game_api

        return env

    def attach_script(self, source, engine_api, public_vars=None):
        engine_api = {
            "SceneManager" : {
                "load_scene" : scene_manager.load_scene,
                "get_current_scene" : scene_manager.get_current_scene,
                "get_scenes" : scene_manager.get_scenes,
                "get_current_cameras" : scene_manager.get_current_cameras,
            },
            "Object" : {
                "get_self" : self.get_parent
            }
        }
        
        with self.lock.gen_wlock():
        
            # Add engine API to Lua environment
            proj_path = self.config_manager.get_config()["projects_path"]
            proj = scene_manager.get_current_proj()


            self.source = source
            path = proj_path + "/" + proj + "/scripts/" + source
            self.engine_api = engine_api

            # Read script file and subscribe to events

            with (open(path, 'r')) as file:
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

    def run_function(self, func_name, *args):
        with self.lock.gen_rlock():
            if self.globals and func_name in self.globals:
                func = self.globals[func_name]
                if callable(func):
                    return func(*args)
                else:
                    raise TypeError(f"Function '{func_name}' is not callable.")
            else:
                raise RuntimeError(f"Function '{func_name}' not found in script context.")
        
    def to_dict(self):
        with self.lock.gen_rlock():

            base = super().to_dict()
            base.update({
                "source": self.source,
                "public_vars": self.public_vars,
            })
            return base

    @classmethod
    def from_dict(cls, data, scene_manager):

        name = data.get("name", "Script")
        source = data.get("source")
        public_vars = data.get("public_vars", {})
        script = Script(name=name)
        engine_api = {
            "SceneManager" : {
                "load_scene" : scene_manager.load_scene,
                "get_current_scene" : scene_manager.get_current_scene,
                "get_scenes" : scene_manager.get_scenes,
                "get_current_cameras" : scene_manager.get_current_cameras,
            },
            "Object" : {
                "get_self" : script.get_parent
            }
        }
        script.attach_script(source, engine_api, public_vars=public_vars)
        return script
