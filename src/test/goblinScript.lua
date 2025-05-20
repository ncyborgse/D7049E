function onAttack(target, damage)
    print("Attacking target: " .. target.get_name() .. " for " .. damage .. " damage")
end

function onKeyPress(key)
    print("Key pressed: " .. key)
    -- Find the tile the goblin is on
    local goblin = game.Object.get_self()
    local goblinTileNode = goblin.get_parent()
    local goblinTile = goblinTileNode.get_component("Tile")

    coords = goblinTile.get_coords()
    local tile_neighbors = goblinTile.get_neighbors()

    --print(coords[1] .. ", " .. coords[2])
    --[[
    for i = 1, 4 do
        local neighbor = tile_neighbors[i]
        if neighbor ~= nil then
            print("Neighbor " .. i .. ": " .. neighbor.get_coords()[1] .. ", " .. neighbor.get_coords()[2])
        else 
            print("Neighbor " .. i .. ": nil")
        end
    end
    ]]--

    local index = nil
    if key == "RIGHT" then
        index = 1
    end
    if key == "UP" then
        index = 2
    end
    if key == "LEFT" then
        index = 3 
    end
    if key == "DOWN" then
        index = 4
    end

    if index ~= nil then
        print("Index: " .. index)
    else 
        return
    end



    if tile_neighbors[index] ~= nil then
        local newTile = tile_neighbors[index]
        local tileNode = newTile.get_parent()

        goblin.attach(tileNode)
    end
end