from scene.component.component import Component
from core.component_registry import register_component
from readerwriterlock import rwlock
from core.global_scene_manager import scene_manager
from scene.component.components.tile import Tile

from scene.component.components.attackable import Attackable

@register_component
class Attacker(Component):
    def __init__(self, name="Attacker"):
        super().__init__(name=name)
        self.attack_power = 10
        self.attack_range = 5.0
        self.lock = rwlock.RWLockFair()

    def subscribe(self, event_emitter):
        pass

    def attack(self, target):
        target_component = target.get_component("Attackable")
        if not target_component:
            raise ValueError("Target does not have an Attackable component.")

        if not self.attack_possible(target):
            raise ValueError("Target cannot be attacked.")
            # Calculate damage and apply it to the target

        damage = self.calculate_damage()
        parent = self.get_parent()

        parent.call_event("onAttack", target, damage)
        target_component.take_damage(damage)

    def attack_possible(self, target):
        # Check if the target has attackable component

        target_component = target.get_component("Attackable")
        if not target_component:
            return False

        # Check with the navigation manager if the target is within attack range
        grid_system = scene_manager.get_grid_system()
        grid = grid_system.get_grid()
        if not grid:
            return False
        
        # Check if any of tagets ancestors are on a tile

        parent = target.get_parent()
        tile = None
        while parent:
            for component in parent.get_components():
                if isinstance(component, Tile):
                    tile = component
                    break
            parent = parent.get_parent()

        if not tile:
            return False
        
        # Check if the attacker is on a tile
        attacker_tile = None
        parent = self.get_parent()
        while parent:
            for component in parent.get_components():
                if isinstance(component, Tile):
                    attacker_tile = component
                    break
            parent = parent.get_parent()


        if not attacker_tile:
            return False
        
        visible = grid_system.is_visible(attacker_tile, tile)
        distance = grid_system.distance(attacker_tile, tile)


        with self.lock.gen_rlock():
            att_range = self.attack_range

        return visible and distance <= att_range

    def calculate_damage(self):
        with self.lock.gen_rlock():
            return self.attack_power

    def set_attack_power(self, attack_power):
        with self.lock.gen_wlock():
            if attack_power < 0:
                raise ValueError("Attack power cannot be negative.")
            self.attack_power = attack_power
    
    def set_attack_range(self, attack_range):
        with self.lock.gen_wlock():
            if attack_range <= 0:
                raise ValueError("Attack range must be greater than 0.")
            self.attack_range = attack_range

    def get_attack_power(self):
        with self.lock.gen_rlock():
            return self.attack_power

    def get_attack_range(self):
        with self.lock.gen_rlock():
            return self.attack_range

    def to_dict(self):
        base = super().to_dict()
        with self.lock.gen_rlock():
            base.update({
                "attack_power": self.attack_power,
                "attack_range": self.attack_range
            })
            return base

    @classmethod
    def from_dict(cls, data, scene_manager):
        instance = cls(name=data.get("name", "Attacker"))
        instance.attack_power = data.get("attack_power", 10)
        instance.attack_range = data.get("attack_range", 5.0)
        return instance