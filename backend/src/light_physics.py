"""Implementation of the most basic physics that i need for the game. Made this
because the game is really simple and i don't really need to load the cpu with box2d worlds.

Notes:
    All bodies coordinates need to be calculated based on the center of the body.
"""
import math
from src.light_numba_functions import *
from src.utils import utils

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
    def __init__(self, x, y, w, h, groupIndex=0):
        super().__init__(x, y, w, h, groupIndex)


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
        self.last_correction = (0,0)

    def circle_circle_collide(self, circle: "Circle"):
        if(self.groupIndex != 0 and self.groupIndex == circle.groupIndex):
            return False
        x_dist = abs(self.x - circle.x)
        y_dist = abs(self.y - circle.y)
        center_dist = (x_dist**2 + y_dist**2)
        radius_sum = self.radius + circle.radius

        return center_dist <= radius_sum * radius_sum # lets just compare to its squared to avoid using sqrt

    def circle_rect_collide(self, rect: Rect):
        if(self.groupIndex != 0 and self.groupIndex == rect.groupIndex):
                    return False
        closest_x = utils.clamp(self.x, rect.x - rect._hw, rect.x + rect._hw)
        closest_y = utils.clamp(self.y, rect.y - rect._hh, rect.y + rect._hh)
        x_dist = self.x - closest_x
        y_dist = self.y - closest_y
        center_dist = (x_dist**2 + y_dist**2)
        return center_dist <= self.radius * self.radius

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
        x, y, vx, vy = bounce_on_rect_numba(self.x, self.y, self.radius,
                                            self.velocity[0],
                                            self.velocity[1],
                                            rect.x, rect.y, rect._hw, rect._hh)
        self.x = x
        self.y = y
        return (vx,vy)

    def reapply_correction(self):
        self.x += self.last_correction[0]
        self.y += self.last_correction[1]


    def update(self, dt):
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt




class LP_Tank(Circle):
    def __init__(self, id, x, y, wh, groupIndex=0):
        super().__init__(x, y, 0, wh / 2, groupIndex)
        self.id = id
        self.wh = wh  # tanks will be represented as circles of radius wh/2
        self.is_shooting = False
        self.groupIndex = groupIndex
        self._needs_to_shoot = False

    def move_to_target(self, x, y, is_shooting=False):
        self._needs_to_shoot = is_shooting
        dx = x - self.x
        dy = y - self.y

        self.angle = math.atan2(dy, dx)

        mag_sq = dx**2 + dy**2
        topSpeed = 1500
        if mag_sq >= self.wh * self.wh and not is_shooting:
            mag = math.sqrt(mag_sq) # lets use sqrt once we actually decided to move
            normDx = dx / mag
            normDy = dy / mag
            ds = (mag * 50) / self.wh
            speed = min(topSpeed, ds)
            self.velocity = (speed * normDx, speed * normDy)
        else:
            self.velocity = (0, 0)

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "needs_to_shoot": self._needs_to_shoot
        }


class LP_Bullet(Circle):
    def __init__(self, id, x, y, radius, angle, speed, groupIndex=0):
        super().__init__(x, y, angle, radius, groupIndex)
        self.id = id
        self.angle = angle
        self.speed = speed
        self.velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle
        }
