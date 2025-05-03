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

        self.bullet = physics_manager.create_body(body_type=BodyType.dynamic,
                                                position=utils.vec2_to_world(pos),
                                                fixture_def=b2FixtureDef(
                                                    shape=b2CircleShape(radius=utils.to_world(3)),
                                                    density=0.5,
                                                    friction=0,
                                                    restitution=1,
                                                    groupIndex = groupIndex
                                                ),
                                                bullet=True,
                                                linearVelocity=(speed * self.direction[0], speed * self.direction[1]),
                                                userData=self)
        
        self.isDead = False
        self.bounces_left = 1


    def _update_locals(self):
        self.x, self.y = utils.vec2_to_pixel(self.bullet.position)

        velocity = self.bullet.linearVelocity
        self.speed = utils.to_pixel(velocity.length)

        if velocity.lengthSquared > 0:
            direction_norm = velocity / velocity.length
            self.direction = (direction_norm.x, direction_norm.y)
    
    def get_state(self):
        self._update_locals()
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
        if (self.bounces_left < 0):
            self.isDead = True
        if self.x < 0 or self.x > GAME_WIDTH or self.y < 0 or self.y > GAME_HEIGHT:
            self.isDead = True
        if(self.isDead):
            self.physics_manager.destroy_body(self.bullet)
            return 1
        return 0