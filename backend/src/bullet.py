from Box2D import (b2FixtureDef, b2CircleShape)
from src.utils import utils
import math
from src.settings import *
from src.physics_manager import PhysicsManager, BodyType

class Bullet:
    def __init__(self, id, pos, angle, damage, speed, groupIndex, physics_manager: PhysicsManager):
       # self.shooter = shooter
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.direction = (math.cos(angle), math.sin(angle))
        self.damage = damage
        self.speed = speed
        self.physics_manager = physics_manager

        self.bullet = physics_manager.create_body(body_type=BodyType.dynamic.value,
                                                position=utils.vec2_to_world(pos),
                                                fixture_def=b2FixtureDef(
                                                    shape=b2CircleShape(radius=utils.to_world(3)),
                                                    density=0.5,
                                                    friction=0,
                                                    restitution=0.5,
                                                    groupIndex = groupIndex
                                                ),
                                                bullet=True,
                                                linearVelocity=(speed * self.direction[0], speed * self.direction[1]),
                                                userData=self)
        
        self.isDead = False

    
    def get_state(self):
        return {
            "id": self.id,
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
        if pixel_pos[0] < 0 or pixel_pos[0] > GAME_WIDTH or pixel_pos[1] < 0 or pixel_pos[1] > GAME_HEIGHT:
            self.physics_manager.destroy_body(self.bullet)
            return 1
        if(self.isDead):
            self.physics_manager.destroy_body(self.bullet)
            return 1
        return 0