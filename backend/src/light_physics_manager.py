from src.common_types import EntityType
from src.light_collision_handler import LP_CollisionHandler
from src.light_physics import LP_Bullet, LP_Tank, LP_Wall, LP_Buff
from src.mediator import BaseMediator


class LP_PhysicsManager(BaseMediator):
    def __init__(self, time_step=1 / 60):
        self.time_step = time_step
        self.collision_handler = LP_CollisionHandler()
        self.bodies: dict[EntityType, dict] = {e:{} for e in EntityType}
        self.tanks: dict[int, LP_Tank] = {}
        self.bullets: dict[int, LP_Bullet] = {}
        self.walls: dict[int, LP_Wall] = {}
        self.buffs: dict[int, LP_Buff] = {}
        self.tick = 0
        self.world_state = {"tanks": {}, "bullets": {}, "collisions": []}

    def update(self):
        tanks = list(self.bodies[EntityType.TANK].values())
        bullets = list(self.bodies[EntityType.BULLET].values())
        walls = list(self.walls.values())
        buffs = list(self.bodies[EntityType.BUFF].values())

        for bullet in bullets:
            bullet.update(self.time_step)

        for tank in tanks:
            tank.update(self.time_step)

        collisions = self.collision_handler.get_latest_collisions(tanks, bullets, walls, buffs)
        self.tick += 1

        return collisions

    def create_wall(self, id, x, y, width, height):
        if id in self.walls:
            raise ValueError(f"Wall with id {id} already exists")
        self.walls[id] = LP_Wall(x, y, width, height)

    def create_body(self, type, **kwargs):
        body = None
        match type:
            case EntityType.TANK:
                body = self._create_tank(**kwargs)
            case EntityType.BULLET:
                body = self._create_bullet(**kwargs)
            case EntityType.WALL:
                body = self._create_wall(**kwargs)
            case EntityType.BUFF:
                body = self._create_buff(**kwargs)
            case _:
                raise ValueError("No such body type")

        self.bodies[type][body.id] = body
        return body

    def _create_tank(self, id, pos, dim):
        if id in self.bodies[EntityType.TANK]:
            raise ValueError(f"Tank with id {tank_id} already exists.")
        ntank = LP_Tank(id,
                        pos[0],
                        pos[1],
                        dim[0],
                        -id)
        return ntank

    def _create_bullet(self, id, pos, angle, speed, radius=3, groupIndex=0, **kwargs):
        if id in self.bodies[EntityType.BULLET]:
            raise ValueError(f"Bullet with id {id} already exists")
        nbullet = LP_Bullet(id,
                            pos[0],
                            pos[1],
                            radius,
                            angle,
                            speed*10,
                            groupIndex)
        return nbullet

    def _create_wall(self, id, x, y, width, height):
        if id in self.bodies[EntityType.WALL]:
            raise ValueError(f"Wall with id {id} already exists")
        nwall = LP_Wall(x,
                        y,
                        width,
                        height)
        return nwall

    def _create_buff(self, id, pos):
        if id in self.bodies[EntityType.BUFF]:
            raise ValueError(f"Buff with id {id} already exists")
        nbuff = LP_Buff(id,
                        pos[0],
                        pos[1],
                        6)
        return nbuff

    def cleanup_world(self, entities_to_destroy):
        tanks_to_destroy = entities_to_destroy["tanks"]
        bullets_to_destroy = entities_to_destroy["bullets"]
        for tank_id in tanks_to_destroy:
            if tank_id in self.tanks:
                del self.tanks[tank_id]

        for bullet_id in bullets_to_destroy:
            if bullet_id in self.bullets:
                del self.bullets[bullet_id]

    def destroy_body(self, id, type):
        if type == EntityType.BULLET:
            if id in self.bullets:
                del self.bullets[id]
                return
        if id in self.bodies[type]:
            del self.bodies[type][id]


