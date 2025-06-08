from abc import ABC, abstractmethod

class Buff(ABC):
    def __init__(self, id):
        self.id = id
    @abstractmethod
    def apply(self, tank):
        pass

class CoolDownBuff(Buff):
    def apply(self, tank):
        tank.cooldown /= 2

class HealthBuff(Buff):
    def apply(self, tank):
        if tank.health >= 90:
            tank.health = 100
            return
        tank.health += 10
