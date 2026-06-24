from src.tank import Tank
from src.bullet import Bullet
from src.settings import *
from src.common_types import EntityType
from src.utils import utils
from src.mediator import BaseMediator
from src.repository import BuffRepo


class EntityManager(BaseMediator):
    def __init__(self):
        self.tanks: dict[int, Tank] = {}
        self.bullets: dict[int, Bullet] = {}
        self.bullet_id_counter = 0
        self.last_world_state = {"tanks": {}, "bullets": {}, "buffs": {}, "collisions": []}
        self.buff_repo = BuffRepo()

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return
        def shoot_callback(owner_id, pos, angle, damage, speed):
            self.spawn_bullet(owner_id, pos, angle, damage, speed)

        logic_tank = Tank(id=player.id, name=player.name,
                                     color=player.color,
                                     shoot_callback=shoot_callback,
                                     )

        self._mediator.notify("CreateBody",
                              type=EntityType.TANK,
                              logic_entity=logic_tank,
                              pos=pos,
                              dim=(TANK_WIDTH, TANK_HEIGHT))
        self.tanks[player.id] = logic_tank

    def spawn_bullet(self, owner_id, pos, angle, damage, speed):
        logic_bullet = Bullet(self.bullet_id_counter,
                              owner_id,
                              damage,
                              )
        self._mediator.notify("CreateBody",
                              type=EntityType.BULLET,
                              logic_entity=logic_bullet,
                              pos=pos,
                              angle=angle,
                              speed=speed,
                              groupIndex=-owner_id)
        self.bullets[logic_bullet.id] = logic_bullet
        self.bullet_id_counter += 1

    def spawn_buff(self, pos):
        logic_buff = self.buff_repo.add_random()
        self._mediator.notify("CreateBody",
                              type=EntityType.BUFF,
                              logic_entity=logic_buff,
                              pos=pos)

    def remove(self, entity):
        try:
            self._mediator.notify("DestroyBody", id=entity.id, type=entity.entity_type)
            match entity.entity_type:
                case EntityType.TANK:
                    del self.tanks[entity.id]
                case EntityType.BULLET:
                    del self.bullets[entity.id]
        except Exception as e:
            utils.logger.warning(f"EntityManager: Couldn't remove {entity.entity_type}, got: {e}")

    def remove_buff(self, id):
        try:
            self._mediator.notify("DestroyBody", id=id, type=EntityType.BUFF)
            self.buff_repo.remove(id)
        except Exception as e:
            utils.logger.warning(f"EntityManager: Couldn't remove buff, got: {e}")

    def get_last_state(self):
        state = {'tanks': {}, 'bullets': {}, 'buffs': {}, 'game_over': False}
        state['buffs'] = self.buff_repo.get_diff_states()
        self.buff_repo.cleanup(self.remove_buff)

        for bullet_id, bullet in list(self.bullets.items()):
            bullet_state, same_state = bullet.get_state_and_diff()
            if not same_state and bullet_state:
                state['bullets'][bullet_id] = bullet_state
            if bullet_state["is_dead"]:
                self.remove(bullet)

        for tank_id, tank in list(self.tanks.items()):
            tank_state, same_state = tank.get_state_and_diff()
            if not same_state and tank_state:
                state['tanks'][tank_id] = tank_state
            if tank.shooting:
                tank.shoot()
            if tank_state["is_dead"]:
                self.remove(tank)

        if len(self.tanks) == 1:
            state['game_over'] = True
            state['winner_id'] = next(iter(self.tanks.keys()))
            state['winner_name'] = self.tanks[state['winner_id']].name

        if state['tanks'] == {} and state['bullets'] == {} and state['buffs'] == {} and not state['game_over']:
            return None
        return state
