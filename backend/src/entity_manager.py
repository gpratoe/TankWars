from src.tank import Tank
from src.bullet import Bullet
from src.settings import *
from src.physics_manager import PhysicsManager
from enum import Enum
from src.common_types import CollisionType

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
        self.last_world_state = {"tanks": {}, "bullets": {}, "collisions": []}
        self.entities_to_destroy = {"tanks": [], "bullets": []}

    def add_tank(self, player, pos, angle):
        if player.id in self.tanks:
            return
        body = self.physics_manager.create_tank(player.id,
                                                pos,
                                                (TANK_WIDTH, TANK_HEIGHT),
                                                )
        def shoot_callback(owner_id, pos, angle, damage, speed):
            self.spawn_bullet(owner_id, pos, angle, damage, speed)

        self.tanks[player.id] = Tank(id=player.id, name=player.name,
                                     color=player.color,
                                     shoot_callback=shoot_callback,
                                     physics_body=body)

    def spawn_bullet(self, owner_id, pos, angle, damage, speed):
        body = self.physics_manager.create_bullet(self.bullet_id_counter,
                                                  pos,
                                                  angle,
                                                  speed,
                                                  groupIndex=-owner_id,
                                                  )
        
        self.bullets[self.bullet_id_counter] = Bullet(self.bullet_id_counter,
                                                      owner_id,
                                                      damage,
                                                      physics_body=body
                                                      )
       
        self.bullet_id_counter += 1

    def update(self, collisions):
        #if world_state == self.last_world_state:
        #    return (None, self.entities_to_destroy)
        self.entities_to_destroy = {"tanks": [], "bullets": []}

        self.apply_collisions(collisions)

        state = {'tanks': {}, 'bullets': {}}

        for bullet_id, bullet in list(self.bullets.items()):
            bullet_state, same_state = bullet.get_state_and_diff()
            if not same_state and bullet_state:
                state['bullets'][bullet_id] = bullet_state
            if bullet_state["is_dead"]:
                del self.bullets[bullet_id]

        for tank_id, tank in list(self.tanks.items()):
            tank_state, same_state = tank.get_state_and_diff()
            if not same_state and tank_state:
                state['tanks'][tank_id] = tank_state
            if tank.shooting:
                tank.shoot()
            if tank_state["is_dead"]:
                del self.tanks[tank_id]

        if state['tanks'] == {} and state['bullets'] == {}:
            return (None, self.entities_to_destroy)
        return (state, self.entities_to_destroy)

    def apply_collisions(self,collisions):
        for collision in collisions:
            match collision.type:
                case CollisionType.BULLET_TANK:
                    world_bullet = collision.first
                    world_tank = collision.second
                    render_bullet = self.bullets[world_bullet.id]
                    render_tank = self.tanks[world_tank.id]
                    render_tank.health -= render_bullet.damage
                    render_bullet.is_dead = True
                    if render_tank.health <= 0:
                        render_tank.is_dead = True
                        self.entities_to_destroy["tanks"].append(render_tank.id)
                    self.entities_to_destroy["bullets"].append(world_bullet.id)
                case CollisionType.BULLET_BULLET:
                    world_b1 = collision.first
                    world_b2 = collision.second
                    render_b1 = self.bullets[world_b1.id]
                    render_b2 = self.bullets[world_b2.id]
                    render_b1.is_dead = True
                    render_b2.is_dead = True
                    self.entities_to_destroy["bullets"].append(world_b1.id)
                    self.entities_to_destroy["bullets"].append(world_b2.id)

                case CollisionType.BULLET_WALL:
                    world_bullet = collision.first
                    render_bullet = self.bullets[world_bullet.id]
                    render_bullet.bounces_left -= 1
                    if render_bullet.bounces_left < 0:
                        render_bullet.is_dead = True
                        self.entities_to_destroy["bullets"].append(render_bullet.id) 
                case _:
                    continue
