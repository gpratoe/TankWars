class Bullet:
    def __init__(self, pos, dir_norm, damage, speed):
        self.x = pos[0]
        self.y = pos[1]
        self.direction =  dir_norm
        self.damage = damage
        self.speed = speed

    def update(self):
        # bullet moves linearly in the direction it was shot
        self.x += self.speed * self.dir_norm[0]
        self.y += self.speed * self.dir_norm[1]