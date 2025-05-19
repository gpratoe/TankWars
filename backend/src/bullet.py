from src.utils import utils
from src.settings import *
import time

class Bullet:
    def __init__(self, id, owner_id, damage, physics_body):
        self.id = id
        self.owner_id = owner_id
        self.physics_body = physics_body
        self.damage = damage
        self.is_dead = False
        self.bounces_left = 1

        self.last_state = {
            "x": self.physics_body.x,
            "y": self.physics_body.y,
            "angle": self.physics_body.angle,
            "is_dead": False,
        }

    
    def get_toclient(self):
        return {
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def get_state_and_diff(self):
        new_state = {
            'x': self.physics_body.x,
            'y': self.physics_body.y,
            'angle': self.physics_body.angle,
            'is_dead': self.is_dead,
        }
        same_state = new_state == self.last_state
        self.last_state = new_state
        return self.get_toclient(), same_state
