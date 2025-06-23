from abc import ABC, abstractmethod
from src.buff import Buff, BuffType
from src.common_types import EntityType
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
        self.id_counter = 0

    def add(self, type: BuffType):
        buff = Buff(self.id_counter, type.name, type.value)
        self.entities[self.id_counter] = buff
        self.id_counter += 1
        return buff

    def add_random(self):
        type = random.choice(list(BuffType))
        return self.add(type)

    def get_states(self):
        return { id: buff.get_state() for id, buff in self.entities.items() }

    def cleanup(self, cleanup_func):
        # You need to pass a function(id) to handle each individual buff.
        # Maybe it's not the most clean way of doing this but i didn't want
        # to loop through the dict in entity_manager.

        for id, buff in list(self.entities.items()):
            if buff.taken:
                cleanup_func(id)








