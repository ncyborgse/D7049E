function onStart()
    -- Find node1 and get it's script component

    local node1 = game.SceneGraph.get_by_name_in(game.SceneGraph.get_root(), "Node1")

    print("Before node1")
    local components = node1.get_components()


    local scriptComp = nil

    for i = 1, #components do
        local comp = components[i]

        if (comp.get_name() == "testScript") then
            scriptComp = comp
            break
        end
    end

    print("After node1")

    -- Run the function "printBingus" in the script component

    if (scriptComp ~= nil) then
        scriptComp.run_function("printBingus")
    end
end