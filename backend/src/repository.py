from abc import ABC, abstractmethod
from src.buff import CoolDownBuff, HealthBuff
import random

class BaseRepository(ABC):
    def __init__(self):
        self.entities = {}

    @abstractmethod
    def add(self, **kwargs):
        pass

    def remove(self, id):
        if id in self.entities:
            del self.entities[id]

    def get(self, id):
        return self.entities.get(id)

class BuffRepo(BaseRepository):
    def __init__(self):
        super().__init__()
        self.add("CoolDown", CoolDownBuff(0))
        self.add("Health", HealthBuff(1))

    def add(self, id, buff):
        self.entities[id] = buff

    def get_random(self):
        return random.choice(list(self.entities.values()))



