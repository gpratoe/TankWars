from Box2D import b2Vec2
from src.utils import utils
import math
from src.settings import *
import time
from src.physics_manager import PhysicsManager

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

        self.last_state = {
            'tankx': pos[0],
            'tanky': pos[1],
            'angle': angle,
            'shooting': False,
            'health': self.health,
            'is_dead': self.is_dead,
        }



    def apply_input(self, input):
        '''
        input: {
            'mouseX': mouseX,
            'mouseY': mouseY,
            'shooting': shooting
        }
        '''
        self.mouseX = input['mouseX']
        self.mouseY = input['mouseY']
        self.is_shooting = input['shooting']



    def _update_body_physics(self):
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

    def update_physics(self):
        '''
        This needs to be called only in the update method in the phisycs manager.
        Otherwise might cause problems.
        '''
        self._update_body_physics()
        if self.is_shooting:
            self.shoot()
        self._update_locals()

    def shoot(self):
        # TODO: maybe use just body physics attributes
        if time.time() - self.shoot_time <= self.cooldown:
            return
        
        bullet_pos = (self.pos[0] + self.w/2 * math.cos(self.angle), self.pos[1] + self.h/2 * math.sin(self.angle))
        if self.shoot_callback:
            self.shoot_callback(self.id, bullet_pos, self.angle, self.damage, self.bullet_speed, self.groupIndex)

        self.shoot_time = time.time()
            

    def _update_locals(self):
        self.is_dead = self.health <= 0
        self.pos = (utils.to_pixel(self.tank.position.x), utils.to_pixel(self.tank.position.y))
        self.angle = self.tank.angle


        
    def get_toclient(self):
        return {
            'name': self.name,
            'color': self.color,
            **self.last_state,
            'timestamp': time.time()*1000,
        }
    
    def update_state_and_diff(self):
        new_state = {
            'tankx': self.pos[0],
            'tanky': self.pos[1],
            'angle': self.angle,
            'shooting': self.is_shooting,
            'health': self.health,
            'is_dead': self.is_dead,
        }
        same_state = new_state == self.last_state
        self.last_state = new_state
        return new_state, same_state