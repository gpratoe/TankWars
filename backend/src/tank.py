import numpy as np
from src.bullet import Bullet

class Tank:
    def __init__(self, name, pos, direction, damage, bullet_speed):
        self.name = name
        self.health = 100
        self.pos = pos
        self.direction = np.array(direction)
        self.direction = self.direction / np.linalg.norm(self.direction)
        self.alive_bullets = []
        self.damage = damage
        self.bullet_speed = bullet_speed


    def shoot(self):
        self.alive_bullets.append(Bullet(self.pos, self.direction, self.damage, self.bullet_speed))
        
    def update_pos(self, new_pos, new_dir):
        self.pos = new_pos
        self.direction = new_dir