from Box2D import (b2FixtureDef, b2PolygonShape, b2Vec2)
from src.bullet import Bullet
from src.utils import utils
import math

class Tank:
    def __init__(self, name, pos, w, h, angle, damage, bullet_speed):
        self.name = name
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
        self.damage = damage
        self.bullet_speed = bullet_speed
        self.tank = utils.world.CreateStaticBody(
            position=utils.vec2_to_world(pos),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world(self.dimentions)),
                density=2,
                friction=0.5,
                restitution=0.1
            ))
        self.tank.userData = self

    def shoot(self):
        bullet_pos = (self.pos[0] + 55 * math.cos(self.angle), self.pos[1] + 55 * math.sin(self.angle))
        self.alive_bullets.append(Bullet(bullet_pos, self.angle, self.damage, self.bullet_speed))
        
    def update(self):
        '''
        Updates the tank's position, direction and if it is shooting
        Needs to modify the tank's mousex, mousey and is_shooting first
        '''
        dx = self.mouseX - utils.to_pixel(self.tank.position.x)
        dy = self.mouseY - utils.to_pixel(self.tank.position.y)

        self.angle = math.atan2(dy, dx)

        # update tank in world
        self.tank.angle = self.angle

        mag = math.sqrt(dx**2 + dy**2)
        topSpeed = 25
        if mag >= self.w  and not self.is_shooting:
            normDx = dx/mag
            normDy = dy/mag
            ds = (mag*5) / self.w
            speed = topSpeed if ds > topSpeed else ds
            self.pos = (utils.to_pixel(self.tank.position.x) + speed * normDx, utils.to_pixel(self.tank.position.y) + speed * normDy)
            # update tank in world
            self.tank.position = utils.vec2_to_world(b2Vec2(self.pos[0], self.pos[1]))
        
        if self.is_shooting:
            #bug cuando dispara se mueve rarinrarin
            self.shoot()
            pass
        for bullet in self.alive_bullets:
            if bullet.update():
                self.alive_bullets.remove(bullet)
        
    def get_state(self):
        return {
            'name': self.name,
            'tankx': utils.to_pixel(self.tank.position.x),
            'tanky': utils.to_pixel(self.tank.position.y),
            'mousex': self.mouseX,
            'mousey': self.mouseY,
            'angle': self.tank.angle,
            'shooting': self.is_shooting,
            'health': self.health
        }
        
    def set_state(self, state):
        self.mouseX = state['mouseX']
        self.mouseY = state['mouseY']
        #self.pos = (state['tankx'], state['tanky'])
        self.is_shooting = state['shooting']