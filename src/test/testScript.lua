
function onStart()
    print("BingusBoss onStart")
    print("Hello BingusWorld!")
    print("Bingus")
end

function onUpdate(deltaTime)
    print("BingusBoss onUpdate" .. tostring(deltaTime))
end

function printBingus()
    print("Bingus")
end

function overlap(nodes)
    local firstNode = nodes[1]
    local nodeName = firstNode.get_name()
    print("BingusBoss overlap: " .. nodeName)