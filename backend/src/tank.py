from src.utils import utils
import math
from src.settings import *
import time

class Tank:
    def __init__(self, id, name, color, shoot_callback, physics_body):
        self.id = id
        self.physics_body = physics_body
        self.name = name
        self.color = color
        self.health = 100
        self.damage = TANK_INITIAL_DAMAGE
        self.bullet_speed = TANK_INITIAL_BULLETSPEED
        self.cooldown = 0.5
        self.shoot_time = 0
        self.is_dead = False
        self.shoot_callback = shoot_callback
        self.shooting = False

        self.last_state = {
            'tankx': physics_body.x,
            'tanky': physics_body.y,
            'angle': physics_body.angle,
            'shooting': False,
            'health': self.health,
            'is_dead': self.is_dead,
        }



    def shoot(self):
        if time.time() - self.shoot_time <= self.cooldown:
            return
        
        bullet_pos = (self.physics_body.x + self.physics_body.wh/2 * math.cos(self.physics_body.angle), self.physics_body.y + self.physics_body.wh/2 * math.sin(self.physics_body.angle))
        if self.shoot_callback:
            self.shoot_callback(self.id, bullet_pos, self.physics_body.angle, self.damage, self.bullet_speed)

        self.shoot_time = time.time()


        
    def get_toclient(self):
        return {
            'name': self.name,
            'color': self.color,
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def get_state_and_diff(self):
        self.shooting = self.physics_body._needs_to_shoot
        new_state = {
            'tankx': self.physics_body.x,
            'tanky': self.physics_body.y,
            'angle': self.physics_body.angle,
            'shooting': self.physics_body._needs_to_shoot,
            'health': self.health,
            'is_dead': self.is_dead,
        }
        same_state = new_state == self.last_state
        self.last_state = new_state
        return self.get_toclient(), same_state
