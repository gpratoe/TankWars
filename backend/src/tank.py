from Box2D import (b2FixtureDef, b2PolygonShape, b2Vec2)
from src.bullet import Bullet
from src.utils import utils
import math
from src.settings import *
import time
from src.physics_manager import PhysicsManager, BodyType

class Tank:
    def __init__(self, id, name, color, pos, w, h, angle, physics_manager: PhysicsManager):
        self.id = id
        self.name = name
        self.color = color
        self.dimentions = b2Vec2(w,h)
        self.health = 100
        self.pos = pos
        self.w = w
        self.h = h
        self.mouseX = pos[0]
        self.mouseY = pos[1]
        self.is_shooting = False
        self.angle = angle
        self.alive_bullets = []
        self.damage = TANK_INITIAL_DAMAGE
        self.bullet_speed = TANK_INITIAL_BULLETSPEED
        self.groupIndex = -id
        self.cooldown = 0.5
        self.shoot_time = 0
        self.bullet_id_counter = 0
        self.is_dead = False

        self.physics_manager = physics_manager
        self.tank = physics_manager.create_body(body_type=BodyType.dynamic,
                                                position=utils.vec2_to_world(pos),
                                                fixture_def=b2FixtureDef(
                                                    shape=b2PolygonShape(box=utils.vec2_to_world(self.dimentions * 0.5)), # * 0.5 because box2d uses half width and half height (almost went insane over this)
                                                    density=2,
                                                    friction=0.5,
                                                    groupIndex=self.groupIndex 
                                                ),
                                                userData=self
                                                )

    def shoot(self):
        if time.time() - self.shoot_time <= self.cooldown:
            return
        
        bullet_pos = (self.pos[0] + self.w * math.cos(self.angle), self.pos[1] + self.h * math.sin(self.angle))
        self.alive_bullets.append(Bullet(self.bullet_id_counter, bullet_pos, self.angle, self.damage, self.bullet_speed, self.groupIndex, self.physics_manager))
        
        self.bullet_id_counter += 1
        self.shoot_time = time.time()

    def update(self):
        '''
        Updates the tank's position, direction and if it is shooting
        Needs to modify the tank's mousex, mousey and is_shooting first
        '''
        if self.health <= 0:
            self.is_dead = True
        
        # calculate angle to where the mouse is
        dx = self.mouseX - utils.to_pixel(self.tank.position.x)
        dy = self.mouseY - utils.to_pixel(self.tank.position.y)

        self.angle = math.atan2(dy, dx)

        # update tank in world
        self.tank.angle = self.angle

        mag = math.sqrt(dx**2 + dy**2)
        topSpeed = 150
        if mag >= self.w and not self.is_shooting:
            normDx = dx/mag
            normDy = dy/mag
            ds = (mag*5) / self.w
            speed = min(topSpeed, ds)
            self.tank.linearVelocity = (speed * normDx, speed * normDy)
        else:
            self.tank.linearVelocity = (0, 0)

        # Actualizar posición local
        self.pos = utils.vec2_to_pixel(self.tank.position)
            
        if self.is_shooting:
            self.shoot()

        
    def get_state(self):
        return {
            'name': self.name,
            'color': self.color,
            'tankx': utils.to_pixel(self.tank.position.x),
            'tanky': utils.to_pixel(self.tank.position.y),
            'mousex': self.mouseX,
            'mousey': self.mouseY,
            'angle': self.angle,
            'shooting': self.is_shooting,
            'health': self.health,
            'is_dead': self.is_dead,
        }
        
    def set_state(self, state):
        self.mouseX = state['mouseX']
        self.mouseY = state['mouseY']
        #self.pos = (state['tankx'], state['tanky'])
        self.is_shooting = state['shooting']