from Box2D import b2Body
from src.utils import utils 
import math
from src.collision_handler import CollisionType

class TankPhysics:
    def __init__(self, id, w, h, body: b2Body):
        self.id = id
        self.body = body
        self.w = w
        self.h = h
        self.type = CollisionType.TANK
        self.body.userData = self
        self.need_to_shoot = False

    def move_to_target(self, target, is_shooting=False):
        dx = target[0] - self.body.position.x
        dy = target[1] - self.body.position.y

        angle = math.atan2(dy, dx)
        self.body.transform = (self.body.position, angle)

        mag = math.sqrt(dx**2 + dy**2)
        topSpeed = 150
        if mag >= self.w and not is_shooting:
            normDx = dx/mag
            normDy = dy/mag
            ds = (mag*5) / self.w
            speed = min(topSpeed, ds)
            self.body.linearVelocity = (speed * normDx, speed * normDy)
        else:
            self.body.linearVelocity = (0, 0)

    def apply_input(self, input):
        """
        To be called just before taking a world step
        """
        mouseX = input['mouseX']
        mouseY = input['mouseY']
        is_shooting = input['shooting']
        target = utils.vec2_to_world((mouseX, mouseY))
        self.move_to_target(target, is_shooting)
        self.need_to_shoot = is_shooting



    def to_dict(self):
        return {
            'tankx': self.body.position.x,
            'tanky': self.body.position.y,
            'angle': self.body.angle,
            'need_to_shoot': self.need_to_shoot,
        }