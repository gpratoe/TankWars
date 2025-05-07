from Box2D import (b2FixtureDef, b2CircleShape)
from src.utils import utils
import math
from src.settings import *
from src.physics_manager import PhysicsManager, BodyType
from src.collision_handler import CollisionType
import time

class Bullet:
    def __init__(self, id, owner_id, pos, angle, damage, speed, groupIndex, physics_manager: PhysicsManager):
       # self.shooter = shooter
        self.id = id
        self.owner_id = owner_id
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
        
        self.is_dead = False
        self.collided_with = None
        self.bounces_left = 1


    def _update_locals(self):
        self.x, self.y = utils.vec2_to_pixel(self.bullet.position)

        velocity = self.bullet.linearVelocity
        self.speed = utils.to_pixel(velocity.length)

        if velocity.lengthSquared > 0:
            direction_norm = velocity / velocity.length
            self.direction = (direction_norm.x, direction_norm.y)
    
    def get_state(self):
        prevx = self.x
        prevy = self.y
        prevdir = self.direction
        prevspeed = self.speed
        prevdamage = self.damage
        previs_dead = self.is_dead

        self._update_locals()
        
        same_state =(
            prevx == self.x and
            prevy == self.y and
            prevdir == self.direction and
            prevspeed == self.speed and
            prevdamage == self.damage and
            previs_dead == self.is_dead
        )

        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "x": self.x,
            "y": self.y,
            "direction": self.direction,
            "damage": self.damage,
            "speed": self.speed,
            "is_dead": self.is_dead,
            "timestamp": time.time()*1000,
        }, same_state
    
    def _act_on_collision(self):
        '''
        Checks if the bullet has collided with something and acts accordingly

        '''
        ##
        # The main reason for this function is to avoid the ocasional double collision
        # that box2d generates when the bullet hits a wall, generating a fake double bounce that 
        # leads to the bullet being destroyed when it shouldnt.
        # Something that will happen if i just act on the collision in the ContactListener / CollisionHandler.       

        if self.collided_with is None:
            return
        
        match self.collided_with:
            case CollisionType.TANK:
                self.is_dead = True
            case CollisionType.BULLET:
                self.is_dead = True
            case CollisionType.WALL:
                self.bounces_left -= 1
                if self.bounces_left < 0:
                    self.is_dead = True
            case _:
                pass
        self.collided_with = None

    def update(self):
        '''
        Checks if the bullet is out of bounds and destroys it if it is
        returns 1 if the bullet is out of bounds
        0 otherwise
        '''
        self._act_on_collision()

        if self.x < 0 or self.x > GAME_WIDTH or self.y < 0 or self.y > GAME_HEIGHT:
            self.is_dead = True
        