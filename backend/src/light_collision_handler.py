from src.light_physics import LP_Bullet, LP_Tank, LP_Wall, LP_Buff
from src.common_types import CollisionType, Collision
from src.mediator import BaseMediator

class LP_CollisionHandler(BaseMediator):
    def __init__(self):
        self.active_collisions = set()

    def get_latest_collisions(self, tanks: list[LP_Tank], bullets: list[LP_Bullet], walls: list[LP_Wall], buffs: list[LP_Buff]):
        new_active_collisions = set()
        for tank in tanks:
            for wall in walls:
                if tank.circle_rect_collide(wall):
                    tank.bounce_on_rect(wall)

            for buff in buffs:
                if tank.circle_circle_collide(buff):
                    col = Collision(buff.id, tank.id, CollisionType.BUFF_TANK)
                    new_active_collisions.add(col)
                    if col not in self.active_collisions:
                        self._mediator.notify("Collision", collision=col)

        for i, bullet in enumerate(bullets):
            for wall in walls:
                if bullet.circle_rect_collide(wall):
                    col = Collision(bullet.id, None, CollisionType.BULLET_WALL)
                    new_active_collisions.add(col)
                    if col not in self.active_collisions:
                        self._mediator.notify("Collision", collision=col)
                    bullet.velocity = bullet.bounce_on_rect(wall)

            for tank in tanks:
                if bullet.circle_circle_collide(tank):
                    col = Collision(bullet.id, tank.id, CollisionType.BULLET_TANK)
                    new_active_collisions.add(col)
                    if col not in self.active_collisions:
                        self._mediator.notify("Collision", collision=col)

            for j in range(i + 1, len(bullets)):
                other = bullets[j]
                if bullet.circle_circle_collide(other):
                    col = Collision(bullet.id, other.id, CollisionType.BULLET_BULLET)
                    new_active_collisions.add(col)
                    if col not in self.active_collisions:
                        self._mediator.notify("Collision", collision=col)

        self.active_collisions = new_active_collisions

