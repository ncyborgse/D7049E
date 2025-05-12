
function onStart()
    print("BingusBoss onStart")
    print("Hello BingusWorld!")
    print("Bingus")
end

function onUpdate(deltaTime)
    ---print("BingusBoss onUpdate" .. tostring(deltaTime))
end

function printBingus()
    print("Bingus")
end

function overlap(nodes)
    local firstNode = nodes[0]
    local nodeName = firstNode.get_name()
    --print("BingusBoss overlap: " .. nodeName)
    local sceneGraph = game.SceneManager.get_current_scene()

    local node1 = sceneGraph.get_by_name_in(sceneGraph.get_root(), "Node1")

    -- Move node1 a very small amount to the right

    --[[node1.apply_transform({
        1, 0, 0, 0.02,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    }) --]]
end

function onClick()
    print("Clicked BingusBoss")
end


