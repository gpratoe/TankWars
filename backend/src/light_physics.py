"""Implementation of the most basic physics that i need for the game. Made this
because the game is really simple and i don't really need to load the cpu with box2d worlds.

Notes:
    All bodies coordinates need to be calculated based on the center of the body.
"""
import math

from numba.cuda import target
from src.light_numba_functions import *
from src.utils import utils
from src.common_types import EntityType
from src.mediator import BaseMediator

class Rect:
    def __init__(self, x, y, w, h, groupIndex=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._hw = w/2
        self._hh = h/2
        self.groupIndex = groupIndex


class LP_Wall(Rect):
    def __init__(self, id, x, y, w, h, groupIndex=0):
        super().__init__(x, y, w, h, groupIndex)
        self.id = id
        self.entity_type = EntityType.WALL


class Circle:
    """Circle class to make hitbox for moving objects.
    Attributes:
        float (x): x coordinate to the center of the circle.
        float (y): y coordinate to the center of the circle.
        float (angle): angle where the object is pointing to, used to update object movement.
        float (radius): radius of the circle.
        int (groupIndex): a basic filter for collisions, if two objects have the same groupIndex they won't collide. Default is 0, meaning normal behaviour.
    """

    def __init__(self, x, y, angle, radius, groupIndex=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = angle
        self.groupIndex = groupIndex
        self.velocity = (0,0)

    def circle_circle_collide(self, circle: "Circle"):
        if(self.groupIndex != 0 and self.groupIndex == circle.groupIndex):
            return False
        return circle_circle_collide_numba(float(self.x), float(self.y), float(circle.x),
                                           float(circle.y), float(self.radius), float(circle.radius))

    def circle_rect_collide(self, rect: Rect):
        if(self.groupIndex != 0 and self.groupIndex == rect.groupIndex):
                    return False
        return circle_rect_collide_numba(float(self.x), float(self.y), float(rect.x),
                                         float(rect.y), float(rect._hw), float(rect._hh),
                                         float(self.radius))

    def bounce_on_rect(self, rect: Rect):
        """Calculates the new velocity the circle would have if it was bouncing on a rect.
        It also corrects the position of the circle and places it outside the rect, so if you just want to
        use it as a way to enforce collision but not bounce off, then just call this function but don't set
        the returned velocity.
        Args:
            Rect (rect): The rect to bounce on
        Returns:
            Tuple(float,float): The new velocity
        """
        x, y, vx, vy = bounce_on_rect_numba(float(self.x), float(self.y), float(self.radius),
                                            float(self.velocity[0]), float(self.velocity[1]),
                                            float(rect.x), float(rect.y), float(rect._hw), float(rect._hh))
        self.x = x
        self.y = y
        return (vx,vy)

    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt




class LP_Tank(Circle, BaseMediator):
    def __init__(self, id, x, y, wh, groupIndex=0):
        Circle.__init__(self, x, y, 0, wh / 2, groupIndex)
        self.id = id
        self.wh = wh  # tanks will be represented as circles of radius wh/2
        self.groupIndex = groupIndex
        self.entity_type = EntityType.TANK

    def rotate_towards_target(self, target_x, target_y):
        angle, _, _ = rotate_towards_target_numba(float(target_x), float(target_y), float(self.x), float(self.y))
        self.angle = angle

    def stop_tank(self):
        self.velocity = (0,0)

    def move_to_target(self, x, y):
        angle, dx, dy = rotate_towards_target_numba(float(x), float(y), float(self.x), float(self.y))
        velocity = move_to_target_numba(float(dx), float(dy), float(self.wh))
        self.velocity = velocity
        self.angle = angle

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
        }


class LP_Bullet(Circle, BaseMediator):
    def __init__(self, id, x, y, radius, angle, speed, groupIndex=0):
        Circle.__init__(self, x, y, angle, radius, groupIndex)
        self.id = id
        self.speed = speed
        self.velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
        self.entity_type = EntityType.BULLET

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle
        }

class LP_Buff(Circle, BaseMediator):
    def __init__(self, id, x, y, radius):
        Circle.__init__(self, x, y, 0, radius)
        self.id = id
        self.entity_type = EntityType.BUFF

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
        }
