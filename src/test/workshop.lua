------------ Workshop 1 -------------
-- play a sound, attached to a node with an audio component

function onStart()
    --[[
    local scene = SceneManager.get_loaded_scene()
    local unit = scene.get_by_name("Cannon")
    local components = unit.get_components()
    ]]

    local components = Node.get_components()    -- "Node" = the node that this scrips is attached to
    local audioComp = nil

    for comp in components do
        if (comp.get_name() == "audio") then
            audioComp = comp
        end
    end

    if (audioComp) then
        audioComp.play_sound()
    end
end


------------ Workshop 2 -------------
-- create (cannon) unit, attached to the ui node (button)

--- in button_script.lua ---

building = nil

function on_click()

    local startNode = Node

    -- Get script component from the node
    local components = building.get_components()

    local scriptComp = nil
    for comp in components do
        if (comp.get_name() == "barracks_script") then
            scriptComp = comp
        end
    end

    if (scriptCompt != nil) then
        scriptComp.run_function("spawn_cannon")
    end

end

function set_target(building)
    building = building

    -- UI logic to change look
end



--- in barracks_script.lua ---

function on_click()
    -- Find correct UI node
    local uiNode = SceneManager.get_loaded_scene().get_by_name("barracks_UI")
    local components = Node.get_components()    -- "Node" = the node that this scrips is attached to
    local scriptComp = nil

    for comp in components do
        if (comp.get_name() == "button_script") then
            scriptComp = comp
        end
    end


    -- Run SetTarget on self
    scriptComp.run_function("set_target", self)     -- check libraries
end

function spawn_cannon()
    local cannon = NodeBuilder.build("cannon")
    local scene = SceneManager.get_loaded_scene()

    scene.add_node(cannon)
end