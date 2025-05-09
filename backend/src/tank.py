from Box2D import (b2FixtureDef, b2PolygonShape, b2Vec2)
from src.bullet import Bullet
from src.utils import utils
import math
from src.settings import *
import time
from src.physics_manager import PhysicsManager, BodyType

class Tank:
    def __init__(self, id, name, color, pos, w, h, angle, physics_manager: PhysicsManager, shoot_callback):
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
        self.is_dead = False
        self.shoot_callback = shoot_callback

        self.physics_manager = physics_manager
        self.tank = physics_manager.create_tank(
            position=(utils.to_world(pos[0]), utils.to_world(pos[1])),
            dimentions=self.dimentions,
            groupIndex=self.groupIndex,
            userData=self
        )

    def shoot(self):
        if time.time() - self.shoot_time <= self.cooldown:
            return
        
        bullet_pos = (self.pos[0] + self.w/2 * math.cos(self.angle), self.pos[1] + self.h/2 * math.sin(self.angle))
        if self.shoot_callback:
            self.shoot_callback(self.id, bullet_pos, self.angle, self.damage, self.bullet_speed, self.groupIndex)

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

        self.tank.angle = math.atan2(dy, dx)

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

            
        if self.is_shooting:
            self.shoot()

    def _update_locals(self):
        self.pos = (utils.to_pixel(self.tank.position.x), utils.to_pixel(self.tank.position.y))
        self.angle = self.tank.angle


        
    def get_state(self):
        prevpos = self.pos
        prevangle = self.angle
        self._update_locals()

        same_state = (
            prevpos == self.pos and
            prevangle == self.angle
        )

        return {
            'name': self.name,
            'color': self.color,
            'tankx': utils.to_pixel(self.tank.position.x),
            'tanky': utils.to_pixel(self.tank.position.y),
            'angle': self.angle,
            'shooting': self.is_shooting,
            'health': self.health,
            'is_dead': self.is_dead,
            'timestamp': time.time()*1000,
        }, same_state
        
    def set_state(self, state):
        self.mouseX = state['mouseX']
        self.mouseY = state['mouseY']
        #self.pos = (state['tankx'], state['tanky'])
        self.is_shooting = state['shooting']