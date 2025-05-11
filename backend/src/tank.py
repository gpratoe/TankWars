from src.utils import utils
import math
from src.settings import *
import time

class Tank:
    def __init__(self, id, name, color, pos, w, h, angle, shoot_callback):
        self.id = id
        self.name = name
        self.color = color
        self.health = 100
        self.pos = pos
        self.w = w
        self.h = h
        self.is_shooting = False
        self.angle = angle
        self.damage = TANK_INITIAL_DAMAGE
        self.bullet_speed = TANK_INITIAL_BULLETSPEED
        self.cooldown = 0.5
        self.shoot_time = 0
        self.is_dead = False
        self.shoot_callback = shoot_callback

        self.last_state = {
            'tankx': pos[0],
            'tanky': pos[1],
            'angle': angle,
            'shooting': False,
            'health': self.health,
            'is_dead': self.is_dead,
        }



    def shoot(self):
        if time.time() - self.shoot_time <= self.cooldown:
            return
        
        bullet_pos = (self.pos[0] + self.w/2 * math.cos(self.angle), self.pos[1] + self.h/2 * math.sin(self.angle))
        if self.shoot_callback:
            self.shoot_callback(self.id, bullet_pos, self.angle, self.damage, self.bullet_speed)

        self.shoot_time = time.time()
            

        
    def get_toclient(self):
        return {
            'name': self.name,
            'color': self.color,
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def update_state_and_diff(self, world_state):
        self.pos = utils.vec2_to_pixel((world_state["tankx"], world_state["tanky"]))
        self.angle = world_state["angle"]
        self.shooting = world_state["needs_to_shoot"]

        new_state = {
            'tankx': self.pos[0],
            'tanky': self.pos[1],
            'angle': self.angle,
            'shooting': self.shooting,
            'health': self.health,
            'is_dead': self.is_dead,
        }
        same_state = new_state == self.last_state
        self.last_state = new_state
        return self.get_toclient(), same_state