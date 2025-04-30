import lupa

class LuaProxy:
    def __init__(self, obj, lua):
        self.obj = obj
        self.lua = lua
        
    def __getattr__(self, name):
        attr = getattr(self.obj, name)

        if callable(attr):
            def wrapper(*args, **kwargs):
                py_args = [self.lua_to_py(arg) for arg in args]
                py_kwargs = {k: self.lua_to_py(v) for k, v in kwargs.items()}
                result = attr(*py_args, **py_kwargs)
                return self.py_to_lua(result)
            return wrapper
        else:
            return self.py_to_lua(attr)
        
    def __getitem__(self, key):
        try:
            value = self.obj[key]
            return self.py_to_lua(value)
        except (KeyError, TypeError, IndexError):
            pass

        # Then try attribute access (for objects like your Node)
        try:
            attr = getattr(self.obj, key)
            if callable(attr):
                def wrapper(*args, **kwargs):
                    py_args = [self.lua_to_py(arg) for arg in args]
                    py_kwargs = {k: self.lua_to_py(v) for k, v in kwargs.items()}
                    result = attr(*py_args, **py_kwargs)
                    return self.py_to_lua(result)
                return wrapper
            return self.py_to_lua(attr)
        except AttributeError:
            raise TypeError(f"Key '{key}' not found in object: {self.obj}")
    
    def __call__(self, *args, **kwargs):
        if not callable(self.obj):
            raise TypeError(f"Object '{self.obj}' is not callable.")
        py_args = [self.lua_to_py(arg) for arg in args]
        py_kwargs = {k: self.lua_to_py(v) for k, v in kwargs.items()}
        result = self.obj(*py_args, **py_kwargs)
        return self.py_to_lua(result)

        
    def lua_to_py(self, value):
        lua_type = self.lua.eval('type')(value)

                # If the Lua value is a userdata, we convert it to a Python object
        if isinstance(value, LuaProxy):
            return value.obj
        
        if lua_type == 'table':
            # Determine if its a list or a dict
            # Note: Self references in Lua tables will cause infinite recursion
    
            keys = list(value.keys())

            # Check if all the keys are integers and if they are sequential
            is_array = all(
                isinstance(k, int) and k > 0 for k in keys
            ) and sorted(keys) == list(range(1, len(keys) + 1))
        
            if is_array:
                # Return as python list
                return [self.lua_to_py(value[i]) for i in range(1, len(keys) + 1)]
            else:
                # Return as python dict
                return {
                    self.lua_to_py(k): self.lua_to_py(v) for k, v in value.items()
                }
            
        else:
            return value
    
    def py_to_lua(self, value):
        if isinstance(value, dict):

            # Check that self.lua is a LupaRumtime instance

            tbl = self.lua.table()
            for k, v in value.items():
                tbl[k] = self.py_to_lua(v)
            return tbl
        elif isinstance(value, (list, tuple)):
            tbl = self.lua.table()
            for i, v in enumerate(value):
                tbl[i + 1] = self.py_to_lua(v) # Lua uses 1-based indexing
            return tbl
        elif hasattr(value, '__dict__') or callable(value):
            return LuaProxy(value, self.lua)
        else:
            return value

