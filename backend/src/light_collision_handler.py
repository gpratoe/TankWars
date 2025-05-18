from src.light_physics import LP_Bullet, LP_Tank, LP_Wall
from src.common_types import CollisionType, Collision

class LP_CollisionHandler:
    def __init__(self):
        self.latest_collisions = []

    def get_latest_collisions(self, tanks: list[LP_Tank], bullets: list[LP_Bullet], walls: list[LP_Wall]):
        collisions = set()

        for tank in tanks:
            for wall in walls:
                if tank.circle_rect_collide(wall):
                    tank.bounce_on_rect(wall)

        for i, bullet in enumerate(bullets):
            for wall in walls:
                if bullet.circle_rect_collide(wall):
                    collisions.add(Collision(bullet, wall, CollisionType.BULLET_WALL))
                    bullet.velocity = bullet.bounce_on_rect(wall)

            for tank in tanks:
                if bullet.circle_circle_collide(tank):
                    collisions.add(Collision(bullet, tank, CollisionType.BULLET_TANK))

            for j in range(i + 1, len(bullets)):
                other = bullets[j]
                if bullet.circle_circle_collide(other):
                    collisions.add(Collision(bullet, other, CollisionType.BULLET_BULLET))

        if self.latest_collisions != collisions:
            self.latest_collisions = collisions
            return collisions
        return []

