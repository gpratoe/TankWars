from src.light_physics import LP_Bullet, LP_Tank, LP_Wall
from src.common_types import CollisionType, Collision

class LP_CollisionHandler:
    def __init__(self):
        self.latest_collisions = []

    def get_latest_collisions(self, tanks: list[LP_Tank], bullets: list[LP_Bullet], walls: list[LP_Wall]):
        collisions = set()
        sublist = tanks.copy()
        for tank in tanks:
            for wall in walls:
                if tank.circle_rect_collide(wall):
                    tank.bounce_on_rect(wall)
                    tank.reapply_correction()

        sublist = bullets.copy()
        for bullet in bullets:
            for wall in walls:
                if bullet.circle_rect_collide(wall):
                    new_collision = Collision(bullet, wall, CollisionType.BULLET_WALL)
                    collisions.add(new_collision)
                    bullet.velocity = bullet.bounce_on_rect(wall)
                    bullet.reapply_correction()

            for tank in tanks:
                if bullet.circle_circle_collide(tank):
                    if bullet.groupIndex != tank.groupIndex:
                        new_collision = Collision(bullet, tank, CollisionType.BULLET_TANK)
                        collisions.add(new_collision)

            sublist.remove(bullet)
            for s_bullet in sublist:
                if bullet.circle_circle_collide(s_bullet):
                    new_collision = Collision(bullet, s_bullet, CollisionType.BULLET_BULLET)
                    collisions.add(new_collision)

        if self.latest_collisions != collisions:
            self.latest_collisions = collisions
            return collisions
        return []

