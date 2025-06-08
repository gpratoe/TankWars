from abc import ABC, abstractmethod

class Buff(ABC):
    @abstractmethod
    def apply(self, tank):
        pass

class CoolDownBuff(Buff):
    def __init__(self, id):
        self.id = id

    def apply(self, tank):
        tank.cooldown /= 2

