from abc import ABC, abstractmethod
from src.buff import Buff, BuffType
from src.common_types import EntityType
from src.tank import Tank
from src.bullet import Bullet
import random

class BaseRepository(ABC):
    def __init__(self):
        self.entities = {}
    def __getitem__(self, id):
        return self.entities[id]
    def __delitem__(self, id):
        del self.entities[id]
    def __contains__(self,id):
        return id in self.entities
    def __len__(self):
        return len(self.entities)
    def __iter__(self):
        return iter(self.entities.items())

    @abstractmethod
    def add(self, **kwargs):
        pass


class BuffRepo(BaseRepository):
    def __init__(self):
        super().__init__()
        self.id_counter = 0

    def add(self, type: BuffType):
        buff = Buff(self.id_counter, type.name, type.value)
        self.entities[self.id_counter] = buff
        self.id_counter += 1
        return buff

    def add_random(self):
        type = random.choice(list(BuffType))
        return self.add(type)


class TankRepo(BaseRepository):
    def __init__(self):
        super().__init__()

    def add(self, player, callback):
        tank = Tank(id=player.id,
                    name=player.name,
                    color=player.color,
                    shoot_callback=callback)
        self.entities[player.id] = tank
        return tank


class BulletRepo(BaseRepository):
    def __init__(self):
        super().__init__()
        self.id_counter = 0

    def add (self, owner_id, damage):
        id = self.id_counter
        bullet = Bullet(id,
                        owner_id,
                        damage)
        self.entities[id] = bullet
        self.id_counter += 1
        return bullet
