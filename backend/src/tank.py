from Box2D import (b2FixtureDef, b2PolygonShape, b2Vec2)
from src.bullet import Bullet
from src.utils import utils
import math

class Tank:
    def __init__(self, name, pos, w, h, angle, damage, bullet_speed):
        self.name = name
        self.dimentions = b2Vec2(20,10)
        self.health = 100
        self.pos = pos
        self.w = w
        self.h = h
        self.mouseX = 0
        self.mouseY = 0
        self.is_shooting = False
        self.angle = angle
        self.alive_bullets = []
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.tank = utils.world.CreateDynamicBody(
            position=utils.vec2_to_world(pos),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world(self.dimentions)),
                density=1,
                friction=0.3
            ))
        self.tank.userData = self

    def shoot(self):
        self.alive_bullets.append(Bullet(self.pos, self.angle, self.damage, self.bullet_speed))
        
    def update(self):
        '''
        Updates the tank's position, direction and if it is shooting
        Needs to modify the tank's mousex, mousey and is_shooting first
        '''
        dx = self.mouseX - self.pos[0]
        dy = self.mouseY - self.pos[1]

        self.angle = math.atan2(dy, dx)

        # update tank in world
        self.tank.angle = self.angle

        mag = math.sqrt(dx**2 + dy**2)
        topSpeed = 15
        if mag >= self.w  and not self.is_shooting:
            normDx = dx/mag
            normDy = dy/mag
            ds = (mag*5) / self.w
            speed = topSpeed if ds > topSpeed else ds
            self.pos = (self.pos[0] + speed * normDx, self.pos[1] + speed * normDy)
            # update tank in world
            self.tank.linearVelocity = (utils.to_world(self.w * normDx), utils.to_world(self.w * normDy))
        
        if self.is_shooting:
            self.shoot()
        for bullet in self.alive_bullets:
            if bullet.update():
                self.alive_bullets.remove(bullet)
        
    def get_state(self):
        return {
            'name': self.name,
            'tankx': self.pos[0],
            'tanky': self.pos[1],
            'angle': self.angle,
            'health': self.health
        }
        
    def set_state(self, state):
        self.mouseX = state['mouseX']
        self.mouseY = state['mouseY']
        #self.pos = (state['tankx'], state['tanky'])
        self.is_shooting = state['shooting']