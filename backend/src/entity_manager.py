from src.tank import Tank
from src.bullet import Bullet
from src.settings import *
from src.physics_manager import PhysicsManager
from enum import Enum
from src.utils import utils

class EntityType(Enum):
    TANK = 0
    BULLET = 1


class EntityManager:
    def __init__(self, physics_manager: PhysicsManager):
        self.tanks: dict[int, Tank] = {}
        self.bullets: dict[int, Bullet] = {}
        self.physics_manager = physics_manager
        self.bullet_id_counter = 0
        self.tanks_to_remove = []
        self.bullets_to_remove = []
        self.last_world_state = {"tanks": {}, "bullets": {}}

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return
        self.physics_manager.create_tank(player.id,
                                        utils.vec2_to_world(pos),
                                        utils.vec2_to_world((TANK_WIDTH, TANK_HEIGHT)),
                                        )
        def shoot_callback(owner_id, pos, angle, damage, speed, groupIndex):
            self.spawn_bullet(owner_id, pos, angle, damage, speed, groupIndex)

        self.tanks[player.id] = Tank(id=player.id, name=player.name,
                                     color=player.color, pos=pos,
                                     w=TANK_WIDTH, h=TANK_HEIGHT,
                                     angle=angle,
                                     shoot_callback=shoot_callback)

    def spawn_bullet(self, owner_id, pos, angle, damage, speed, groupIndex):
        bullet = Bullet(self.bullet_id_counter, owner_id, pos, angle, damage, speed, groupIndex, self.physics_manager)
        self.bullets.setdefault(self.bullet_id_counter, bullet)
        self.bullet_id_counter += 1

    def cleanup_entities(self):
        for tank_id in self.tanks_to_remove:
            if tank_id in self.tanks:
                del self.tanks[tank_id]
        self.tanks_to_remove.clear()

        for bullet_id in self.bullets_to_remove:
            if bullet_id in self.bullets:
                del self.bullets[bullet_id]
        self.bullets_to_remove.clear()

    def update(self, world_state):
        if world_state == self.last_world_state:
            return None
        self.last_world_state = world_state
        physics_tanks = world_state.get('tanks')
        physics_bullets = world_state.get('bullets')

        state = {'tanks': {}, 'bullets': {}}
        for tank_id, tank in list(self.tanks.items()):
            tank_state, same_state = tank.update_state_and_diff(physics_tanks[tank_id])
            if not same_state and tank_state:
                state['tanks'][tank_id] = tank_state
            if tank.is_dead:
                self.tanks_to_remove.append(tank_id)
        
        # for bullet_id, bullet in list(self.bullets.items()):
        #     bullet.update()
        #     bullet_state, same_state = bullet.get_state()
        #     if not same_state and bullet_state:
        #         state['bullets'][bullet_id] = bullet_state
        #     if bullet.is_dead:
        #         self.bullets_to_remove.append(bullet_id)
        self.cleanup_entities()
        
        if state['tanks'] == {} and state['bullets'] == {}:
            return None
        return state
