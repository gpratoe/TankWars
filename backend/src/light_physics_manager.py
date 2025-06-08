from src.common_types import EntityType
from src.light_collision_handler import LP_CollisionHandler
from src.light_physics import LP_Bullet, LP_Tank, LP_Wall, LP_Buff
from src.mediator import BaseMediator


class LP_PhysicsManager(BaseMediator):
    def __init__(self, time_step=1 / 60):
        self.time_step = time_step
        self.collision_handler = LP_CollisionHandler()
        self.tanks: dict[int, LP_Tank] = {}
        self.bullets: dict[int, LP_Bullet] = {}
        self.walls: dict[int, LP_Wall] = {}
        self.buffs: dict[int, LP_Buff] = {}
        self.tick = 0
        self.world_state = {"tanks": {}, "bullets": {}, "collisions": []}

    def update(self):
        tanks = list(self.tanks.values())
        bullets = list(self.bullets.values())
        walls = list(self.walls.values())
        buffs = list(self.buffs.values())

        for bullet in self.bullets.values():
            bullet.update(self.time_step)

        for tank in self.tanks.values():
            tank.update(self.time_step)

        collisions = self.collision_handler.get_latest_collisions(tanks, bullets, walls, buffs)
        self.tick += 1

        return collisions


    def create_tank(self, tank_id, pos, dim):
        if tank_id in self.tanks:
            raise ValueError(f"Tank with id {tank_id} already exists.")
        ntank = LP_Tank(tank_id, pos[0], pos[1], dim[0], -tank_id)
        self.tanks[tank_id] = ntank
        return ntank

    def create_bullet(self, bullet_id, pos, angle, speed, radius=3, groupIndex=0, **kwargs):
        if bullet_id in self.bullets:
            raise ValueError(f"Bullet with id {bullet_id} already exists")
        nbullet = LP_Bullet(bullet_id, pos[0], pos[1], radius, angle, speed*10, groupIndex)
        self.bullets[bullet_id] = nbullet
        return nbullet

    def create_wall(self, id, x, y, width, height):
        if id in self.walls:
            raise ValueError(f"Wall with id {id} already exists")
        self.walls[id] = LP_Wall(x, y, width, height)

    def create_buff(self, id, pos):
        if id in self.buffs:
            raise ValueError(f"Buff with id {id} already exists")
        self.buffs[id] = LP_Buff(id, pos[0], pos[1], 6)


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
        if type == EntityType.TANK:
            if id in self.tanks:
                del self.tanks[id]
                return
        if type == EntityType.BULLET:
            if id in self.bullets:
                del self.bullets[id]
                return
        if type == EntityType.WALL:
            if id in self.walls:
                del self.walls[id]
                return
        if type == EntityType.BUFF:
            if id in self.buffs:
                del self.buffs[id]
                return

