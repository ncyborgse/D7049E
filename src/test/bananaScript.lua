function onDamageTaken(damage)
    -- Check if the damage is greater than 0
    local attackable_component  = game.Object.get_self().get_component("Attackable")
    if damage > 0 then
        -- Print a message to the console
        local defense = attackable_component.get_defense()
        print("Defense: " .. defense)
        print("Damage taken: " .. damage)
        print("Health: " .. attackable_component.get_health())
    end
end

function onDeath()
    -- Print a message to the console
    print("Banana has died")
    game.Object.get_self().detach()
end

function onClick()
    -- Have the goblin attempt to attack the banana when clicked
    print("Clicked Banana")
    local goblin = game.SceneManager.get_current_scene().get_by_name_in(game.SceneManager.get_current_scene().get_root(), "GoblinNode")
    if goblin ~= nil then
        local goblin_attacker = goblin.get_component("Attacker")
        if goblin_attacker ~= nil then
            local target = game.Object.get_self()
            goblin_attacker.attack(target)
        else
            print("Goblin attacker component not found")
        end
    else
        print("Goblin not found")
    end
end 