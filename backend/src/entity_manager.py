from src.settings import *
from src.common_types import EntityType
from src.utils import utils
from src.mediator import BaseMediator
from src.repository import BuffRepo, TankRepo, BulletRepo


class EntityManager(BaseMediator):
    def __init__(self):
        self.buff_repo = BuffRepo()
        self.tank_repo = TankRepo()
        self.bullet_repo = BulletRepo()


    def add_tank(self, player, pos):
        if player.id in self.tank_repo:
            return
        def shoot_callback(owner_id, pos, angle, damage, speed):
            self.spawn_bullet(owner_id, pos, angle, damage, speed)

        logic_tank = self.tank_repo.add(player=player,
                                        callback=shoot_callback)

        self._mediator.notify("CreateBody",
                              type=EntityType.TANK,
                              logic_entity=logic_tank,
                              pos=pos,
                              dim=(TANK_WIDTH, TANK_HEIGHT))


    def spawn_bullet(self, owner_id, pos, angle, damage, speed):
        logic_bullet = self.bullet_repo.add(owner_id=owner_id,
                                            damage=damage)
        self._mediator.notify("CreateBody",
                              type=EntityType.BULLET,
                              logic_entity=logic_bullet,
                              pos=pos,
                              angle=angle,
                              speed=speed,
                              groupIndex=-owner_id)


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
                case EntityType.TANK: del self.tank_repo[entity.id]
                case EntityType.BUFF: del self.buff_repo[entity.id]
                case EntityType.BULLET: del self.bullet_repo[entity.id]
        except Exception as e:
            utils.logger.warning(f"EntityManager: Couldn't remove {entity.entity_type}, got: {e}")


    def get_init(self):
        """
        Returns initial config.
        To be used in the prev config state.
        """

        return {'tanks':{t.id: t.get_toclient() for _, t in self.tank_repo}}



    def get_last_state(self):
        state = {'tanks': {}, 'bullets': {}, 'buffs': {}, 'game_over': False}

        for id, buff in list(self.buff_repo):
            buff_state, same = buff.get_state_and_diff()
            if not same:
                state["buffs"][id] = buff_state
            if buff.taken:
                self.remove(buff)


        for id, bullet in list(self.bullet_repo):
            bullet_state, same_state = bullet.get_state_and_diff()
            if not same_state and bullet_state:
                state["bullets"][id] = bullet_state
            if bullet_state["is_dead"]:
                self.remove(bullet)


        for id, tank in list(self.tank_repo):
            tank_state, same_state = tank.get_state_and_diff()
            if not same_state and tank_state:
                state["tanks"][id] = tank_state
            if tank.shooting:
                tank.shoot()
            if tank_state["is_dead"]:
                self.remove(tank)

        if len(self.tank_repo.entities) == 1:
            state['game_over'] = True
            state['winner_id'] = next(iter(self.tank_repo))[0]
            state['winner_name'] = self.tank_repo[state['winner_id']].name

        if state['tanks'] == {} and state['bullets'] == {} and state['buffs'] == {} and not state['game_over']:
            return None
        return state
