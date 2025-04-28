from scene.components.script import Script
from pyee import EventEmitter

emitter = EventEmitter()


src = "src/test/testScript.lua"
script = Script()
script.attachScript(src)
script.subscribe(emitter)

emitter.emit("onStart")