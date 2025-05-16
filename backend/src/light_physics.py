"""Implementation of the most basic physics that i need for the game. Made this
because the game is really simple and i don't really need to load the cpu with box2d worlds.

Notes:
    All bodies coordinates need to be calculated based on the center of the body.
"""
import math
from src.utils import utils
import numpy as np


class Rect:
    def __init__(self, x, y, w, h, groupIndex=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
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
        int (groupIndex): a basic filter for collisions, if two objects have the same groupIndex they won't collide.
    """

    def __init__(self, x, y, angle, radius, groupIndex=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = angle
        self.groupIndex = groupIndex
        self.velocity = np.array([0,0])
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
        closest_x = utils.clamp(self.x, rect.x - rect.w / 2, rect.x + rect.w / 2)
        closest_y = utils.clamp(self.y, rect.y - rect.h / 2, rect.y + rect.h / 2)
        x_dist = self.x - closest_x
        y_dist = self.y - closest_y
        center_dist = (x_dist**2 + y_dist**2)
        return center_dist <= self.radius * self.radius

    def bounce_on_rect(self, rect: Rect):
        """Calculates the new velocity the circle would have if it was bouncing on a rect
        Args:
            Rect (rect): The rect to bounce on
        Returns:
            Tuple(float,float): The new velocity
        """
        closest_x = utils.clamp(self.x, rect.x - rect.w/2, rect.x + rect.w/2)
        closest_y = utils.clamp(self.y, rect.y - rect.h/2, rect.y + rect.h/2)

        circle_pos = np.array([self.x, self.y])
        closest_point = np.array([closest_x, closest_y])

        normal_v = circle_pos - closest_point # normal pointing to the closest point in the rect
        norm = np.linalg.norm(normal_v)
        print(norm,normal_v)
        
        if norm == 0:
            dx = self.x - rect.x
            dy = self.y - rect.y

            overlap_x = (rect.w/2 + self.radius) - abs(dx)
            overlap_y = (rect.h/2 + self.radius) - abs(dy)

            if overlap_x < overlap_y:
                normal_v = np.array([np.sign(dx),0])
            else:
                normal_v = np.array([0, np.sign(dy)])
            prct_in = self.radius # percentage of the ball that got "inside" the wall
        else:
            normal_v = normal_v / norm
            prct_in = self.radius - norm

        if prct_in > 0:
            correction = normal_v * prct_in # lets push the ball outside the wall to avoid glitches
            self.x += correction[0]
            self.y += correction[1]

            self.last_correction = correction

        new_vel = self.velocity - 2 * np.dot(self.velocity, normal_v) * normal_v

        return new_vel

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

        mag = math.sqrt(dx**2 + dy**2)
        topSpeed = 1500
        if mag >= self.wh and not is_shooting:
            normDx = dx / mag
            normDy = dy / mag
            ds = (mag * 50) / self.wh
            speed = min(topSpeed, ds)
            self.velocity = np.array([speed * normDx, speed * normDy])
        else:
            self.velocity = np.array([0, 0])

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
        self.velocity = np.array([math.cos(angle) * speed, math.sin(angle) * speed])

    def get_state(self):
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle
        }
