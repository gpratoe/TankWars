from src.utils import utils
from src.settings import *
import time
from src.mediator import BaseMediator

class Bullet(BaseMediator):
    def __init__(self, id, owner_id, damage):
        self.id = id
        self.owner_id = owner_id
        self.damage = damage
        self.is_dead = False
        self.bounces_left = 1

        self.last_state = None

    
    def get_toclient(self):
        return {
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def get_state_and_diff(self):
        new_state = self.get_state()
        same_state = new_state == self.last_state
        self.last_state = new_state
        return self.get_toclient(), same_state

    def get_state(self):
        physics_state = self._mediator.notify("GetPhysicsState")
        physics_state["is_dead"] = self.is_dead
        return physics_state

