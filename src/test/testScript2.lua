function onStart()
    -- Find node1 and get it's script component

    local node1 = game.SceneGraph.get_by_name_in(game.SceneGraph.get_root(), "Node1")


    local components = node1.get_components()


    local scriptComp = nil

    for i = 1, #components do
        local comp = components[i]

        if (comp.get_name() == "Script1") then
            scriptComp = comp
            break
        end
    end

    -- Run the function "printBingus" in the script component

    if (scriptComp ~= nil) then
        print("Found script component")
        scriptComp.run_function("printBingus")
    end
end