from Box2D import (b2FixtureDef, b2CircleShape, b2Vec2)
from src.utils import utils
import math
import copy

class Bullet:
    def __init__(self, pos, angle, damage, speed):
       # self.shooter = shooter
        self.x = pos[0]
        self.y = pos[1]
        self.direction = (math.cos(angle), math.sin(angle))
        self.damage = damage
        self.speed = speed
        self.bullet = utils.world.CreateDynamicBody(
            position=utils.vec2_to_world(b2Vec2(self.x, self.y)),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=1),
                density=0.1,
                friction=0.1,
                restitution=0.5
            ))
        self.bullet.linearVelocity = (self.speed * self.direction[0], self.speed * self.direction[1])
        self.bullet.bullet = True
        
        self.bullet.userData = self
    
    def get_state(self):
        return {
            "x": utils.to_pixel(self.bullet.position.x),
            "y": utils.to_pixel(self.bullet.position.y),
            "direction": self.direction,
            "damage": self.damage,
            "speed": self.speed
        }
    def update(self):
        '''
        Checks if the bullet is out of bounds and destroys it if it is
        returns 1 if the bullet is out of bounds
        0 otherwise
        '''
        pixel_pos = utils.vec2_to_pixel(self.bullet.position)
        if pixel_pos[0] < 0 or pixel_pos[0] > utils.gameWidth or pixel_pos[1] < 0 or pixel_pos[1] > utils.gameHeight:
            utils.world.DestroyBody(self.bullet)
            return 1
        return 0