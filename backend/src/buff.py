from abc import ABC, abstractmethod
from enum import Enum
from src.mediator import BaseMediator

class BuffEffect(ABC):
    @abstractmethod
    def apply(self, tank):
        pass

class CoolDownBuff(BuffEffect):
    def apply(self, tank):
        tank.cooldown /= 2

class HealthBuff(BuffEffect):
    def apply(self, tank):
        if tank.health >= 90:
            tank.health = 100
            return
        tank.health += 10

class BuffType(Enum):
    COOLDOWN = CoolDownBuff()
    HEALTH = HealthBuff()

class Buff(BaseMediator):
    def __init__(self, id, effect: BuffEffect):
        self.id = id
        self.effect = effect
        self.taken = False

    def get_state(self):
        physics_state = self._mediator.notify("GetPhysicsState")
        return {
            'taken': self.taken,
            **physics_state
        }

