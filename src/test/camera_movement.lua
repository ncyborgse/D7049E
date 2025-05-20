function onKeyHold(key, deltaTime)
    local camera = game.SceneManager.get_current_cameras()[1]
    if (camera == nil) then
        print("No camera found")
        return
    end
    local x = 0
    local y = 0
    if (key == "W") then
        y = 2 * deltaTime
    elseif (key == "S") then
        y = -2 * deltaTime
    elseif (key == "A") then
        x = 2 * deltaTime
    elseif (key == "D") then
        x = -2 * deltaTime
    end

    local transform = {1, 0, 0, x,
                       0, 1, 0, y,
                       0, 0, 1, 0,
                       0, 0, 0, 1}

    local cameraNode = camera.get_parent()

    cameraNode.apply_transform(transform)
end