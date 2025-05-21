from src.utils import utils
import math
from src.settings import *
import time
from src.mediator import BaseMediator

class Tank(BaseMediator):
    def __init__(self, id, name, color, shoot_callback):
        self.id = id
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
        self.last_state = None


    def shoot(self, bullet_pos, angle):
        if time.time() - self.shoot_time <= self.cooldown:
            return
        if self.shoot_callback:
            self.shoot_callback(self.id, bullet_pos, angle, self.damage, self.bullet_speed)
        self.shoot_time = time.time()


        
    def get_toclient(self):
        return {
            'name': self.name,
            'color': self.color,
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def get_state_and_diff(self):
        new_state =  self.get_state()
        same_state = new_state == self.last_state
        self.last_state = new_state
        return self.get_toclient(), same_state

    def get_state(self):
        physics_state = self._mediator.notify("GetPhysicsState")
        return {
            'tankx': physics_state["x"],
            'tanky': physics_state["y"],
            'angle': physics_state["angle"],
            'health': self.health,
            'is_dead': self.is_dead
        }
