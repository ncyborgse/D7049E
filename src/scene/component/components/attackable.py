from scene.component.component import Component
from core.component_registry import register_component
from readerwriterlock import rwlock

@register_component
class Attackable(Component):
    def __init__(self, name="Attackable"):
        super().__init__(name=name)
        self.max_health = 100
        self.health = self.max_health
        self.attack_power = 10
        self.defense = 5
        self.alive = True
        self.lock = rwlock.RWLockFair()

    def subscribe(self, event_emitter):
        with self.lock.gen_wlock():
            # Subscribe to events related to attackable entities
            event_emitter.on("onDamageTaken", self.take_damage)
            event_emitter.on("onHeal", self.heal)


    def take_damage(self, damage):
        with self.lock.gen_wlock():
            if not self.alive:
                raise RuntimeError("Cannot take damage, the entity is already dead.")
            damage_taken = max(0, damage - self.defense)
            self.health -= damage_taken
            if self.health <= 0:
                self.die()
    
    def set_max_health(self, max_health):
        with self.lock.gen_wlock():
            if max_health <= 0:
                raise ValueError("Max health must be greater than 0.")
            self.max_health = max_health
            self.health = min(self.health, self.max_health)
    
    def set_defense(self, defense):
        with self.lock.gen_wlock():
            if defense < 0:
                raise ValueError("Defense cannot be negative.")
            self.defense = defense

    def get_health(self):
        with self.lock.gen_rlock():
            return self.health
    
    def get_max_health(self):
        with self.lock.gen_rlock():
            return self.max_health

    def get_defense(self):
        with self.lock.gen_rlock():
            return self.defense

    def is_alive(self):
        with self.lock.gen_rlock():
            return self.alive

    def heal(self, amount):
        with self.lock.gen_wlock():
            if not self.alive:
                raise RuntimeError("Cannot heal, the entity is already dead.")
            self.health = min(self.health + amount, self.max_health)

    def attack(self, target):
        if not isinstance(target, Attackable):
            raise TypeError("Target must be an instance of Attackable.")
        target.take_damage(self.attack_power)

    def die(self):
        self.alive = False

    def to_dict(self):
        with self.lock.gen_rlock():
            return {
                "name": self.name,
                "type": self.__class__.__name__,
                "max_health": self.max_health,
                "health": self.health,
                "defense": self.defense,
                "alive": self.alive
            }

    @classmethod
    def from_dict(cls, data, scene_manager):
        instance = cls(name=data.get("name", "Attackable"))
        instance.max_health = data.get("max_health", 100)
        instance.health = data.get("health", instance.max_health)
        instance.defense = data.get("defense", 5)
        instance.alive = data.get("alive", True)
        return instance

