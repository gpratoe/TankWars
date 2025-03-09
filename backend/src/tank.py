from Box2D import (b2FixtureDef, b2PolygonShape, b2Vec2)
from src.bullet import Bullet
from src.utils import utils
import math
import json
from src.settings import *
import time

class Tank:
    def __init__(self, id, name, color, pos, w, h, angle):
        self.id = id
        self.name = name
        self.color = color
        self.dimentions = b2Vec2(w,h)
        self.health = 100
        self.pos = pos
        self.w = w
        self.h = h
        self.mouseX = 0
        self.mouseY = 0
        self.is_shooting = False
        self.angle = angle
        self.alive_bullets = []
        self.damage = TANK_INITIAL_DAMAGE
        self.bullet_speed = TANK_INITIAL_BULLETSPEED
        self.groupIndex = -id
        self.cooldown = 1
        self.shoot_time = 0

        self.tank = utils.world.CreateKinematicBody(
            position=utils.vec2_to_world(pos),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world(self.dimentions * 0.5)), # * 0.5 because box2d uses half width and half height (almost went insane over this)
                density=2,
                friction=0.5,
                restitution=0.1,
                groupIndex=self.groupIndex 
            ))
        self.tank.userData = self

    def shoot(self):
        self.shoot_time = time.time()
        #bullet_pos = (self.pos[0] + 75 * math.cos(self.angle), self.pos[1] + 75 * math.sin(self.angle))
        bullet_pos = (self.pos[0] + self.w*2 * math.cos(self.angle), self.pos[1] + self.h*2 * math.sin(self.angle))
        self.alive_bullets.append(Bullet(bullet_pos, self.angle, self.damage, self.bullet_speed, self.groupIndex))
        
    def update(self):
        '''
        Updates the tank's position, direction and if it is shooting
        Needs to modify the tank's mousex, mousey and is_shooting first
        '''
        if self.health <= 0:
            utils.world.DestroyBody(self.tank)
            return 1
        dx = self.mouseX - utils.to_pixel(self.tank.position.x)
        dy = self.mouseY - utils.to_pixel(self.tank.position.y)

        self.angle = math.atan2(dy, dx)

        # update tank in world
        self.tank.angle = self.angle

        mag = math.sqrt(dx**2 + dy**2)
        topSpeed = 1.5
        if mag >= self.w+100  and not self.is_shooting:
            normDx = dx/mag
            normDy = dy/mag
            ds = (mag*5) / self.w
            speed = topSpeed if ds > topSpeed else ds
            self.tank.position = (self.tank.position.x + speed * normDx, self.tank.position.y + speed * normDy)
            # update tank in world
            self.pos = utils.vec2_to_pixel(self.tank.position)
            
        if self.is_shooting and time.time() - self.shoot_time > self.cooldown:
            self.shoot()
            pass
        for bullet in self.alive_bullets:
            if bullet.update():
                self.alive_bullets.remove(bullet)
        
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
            'health': self.health
        }
        
    def set_state(self, state):
        self.mouseX = state['mouseX']
        self.mouseY = state['mouseY']
        #self.pos = (state['tankx'], state['tanky'])
        self.is_shooting = state['shooting']