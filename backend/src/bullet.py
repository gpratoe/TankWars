from src.utils import utils
from src.settings import *
import time

class Bullet:
    def __init__(self, id, owner_id, pos, angle, damage, speed):
        self.id = id
        self.owner_id = owner_id
        self.x = pos[0]
        self.y = pos[1]
        self.angle = angle
        self.damage = damage
        self.speed = speed
        self.is_dead = False
        self.bounces_left = 1

        self.last_state = {
            "x": pos[0],
            "y": pos[1],
            "angle": angle,
            "is_dead": False,
        }

    
    def get_toclient(self):
        return {
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def update_state_and_diff(self, world_state):
        self.x = utils.to_pixel(world_state["bulletx"])
        self.y = utils.to_pixel(world_state["bullety"])
        self.angle = world_state["angle"]

        new_state = {
            'x': self.x,
            'y': self.y,
            'angle': self.angle,
            'is_dead': self.is_dead,
        }
        same_state = new_state == self.last_state
        self.last_state = new_state
        return self.get_toclient(), same_state