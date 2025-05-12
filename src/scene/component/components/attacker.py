from scene.component.component import Component
from core.component_registry import register_component
from readerwriterlock import rwlock

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
            raise ValueError("Target is out of range for attack.")
        with self.lock.gen_wlock():
            # Calculate damage and apply it to the target
            damage = self.calculate_damage()
        target.call_event("onDamageTaken", damage)

    def attack_possible(self, target):
        with self.lock.gen_rlock():
            if not isinstance(target, Attackable):
                return False

            # Check with the navigation manager if the target is within attack range (IMPLEMENT LATER)

            return True

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
        with self.lock.gen_rlock():
            return {
                "name": self.name,
                "type": self.__class__.__name__,
                "attack_power": self.attack_power,
                "attack_range": self.attack_range
            }

    @classmethod
    def from_dict(cls, data, scene_manager):
        instance = cls(name=data.get("name", "Attacker"))
        instance.attack_power = data.get("attack_power", 10)
        instance.attack_range = data.get("attack_range", 5.0)
        return instance