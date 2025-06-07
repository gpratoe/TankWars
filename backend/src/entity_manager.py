from src.tank import Tank
from src.bullet import Bullet
from src.settings import *
from src.common_types import CollisionType, EntityType
from src.utils import utils
from src.mediator import BaseMediator


class EntityManager(BaseMediator):
    def __init__(self):
        self.tanks: dict[int, Tank] = {}
        self.bullets: dict[int, Bullet] = {}
        self.bullet_id_counter = 0
        self.tanks_to_remove = []
        self.bullets_to_remove = []
        self.last_world_state = {"tanks": {}, "bullets": {}, "collisions": []}
        self.entities_to_destroy = {"tanks": [], "bullets": []}
        self.dead_players_count = 0

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return
        def shoot_callback(owner_id, pos, angle, damage, speed):
            self.spawn_bullet(owner_id, pos, angle, damage, speed)

        logic_tank = Tank(id=player.id, name=player.name,
                                     color=player.color,
                                     shoot_callback=shoot_callback,
                                     )

        self._mediator.notify("CreateTank",logic_tank=logic_tank, pos=pos, dim=(TANK_WIDTH, TANK_HEIGHT))
        self.tanks[player.id] = logic_tank

    def spawn_bullet(self, owner_id, pos, angle, damage, speed):
        logic_bullet = Bullet(self.bullet_id_counter,
                              owner_id,
                              damage,
                              )
        self._mediator.notify("CreateBullet", logic_bullet=logic_bullet,
                              pos=pos,
                              angle=angle,
                              speed=speed,
                              groupIndex=-owner_id)
        self.bullets[logic_bullet.id] = logic_bullet
        self.bullet_id_counter += 1

    def remove_tank(self, tank):
        try:
            self._mediator.notify("DestroyBody", id=tank.id, type=EntityType.TANK)
            del self.tanks[tank.id]
        except Exception as e:
            utils.logger.warning(f"EntityManager: Couldn't remove tank, got: {e}")

    def remove_bullet(self, bullet):
        try:
            self._mediator.notify("DestroyBody", id=bullet.id, type=EntityType.BULLET)
            del self.bullets[bullet.id]
        except Exception as e:
            utils.logger.warning(f"EntityManager: Couldn't remove bullet, got: {e}")

    def get_last_state(self):
        state = {'tanks': {}, 'bullets': {}, 'game_over': False}

        for bullet_id, bullet in list(self.bullets.items()):
            bullet_state, same_state = bullet.get_state_and_diff()
            if not same_state and bullet_state:
                state['bullets'][bullet_id] = bullet_state
            if bullet_state["is_dead"]:
                self.remove_bullet(bullet)

        for tank_id, tank in list(self.tanks.items()):
            tank_state, same_state = tank.get_state_and_diff()
            if not same_state and tank_state:
                state['tanks'][tank_id] = tank_state
            if tank.shooting:
                tank.shoot()
            if tank_state["is_dead"]:
                self.remove_tank(tank)


        if len(self.tanks) == 1:
            state['game_over'] = True
            state['winner_id'] = next(iter(self.tanks.keys()))
            state['winner_name'] = self.tanks[state['winner_id']].name

        if state['tanks'] == {} and state['bullets'] == {} and not state['game_over']:
            return None
        return state

    def handle_collision(self,collision):
            first_id = collision.first
            second_id = collision.second
            match collision.type:
                case CollisionType.BULLET_TANK:
                    bullet = self.bullets[first_id]
                    tank = self.tanks[second_id]
                    tank.health -= bullet.damage
                    bullet.is_dead = True
                    if tank.health <= 0:
                        tank.is_dead = True
                case CollisionType.BULLET_BULLET:
                    b1 = self.bullets[first_id]
                    b2 = self.bullets[second_id]
                    b1.is_dead = True
                    b2.is_dead = True
                case CollisionType.BULLET_WALL:
                    bullet = self.bullets[first_id]
                    bullet.bounces_left -= 1
                    if bullet.bounces_left < 0:
                        bullet.is_dead = True
                case _:
                    pass
