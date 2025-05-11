from Box2D import b2World, b2FixtureDef, b2PolygonShape, b2CircleShape, b2Vec2
from enum import IntEnum
from src.collision_handler import CollisionHandler
from src.tank_physics import TankPhysics
from src.bullet_physics import BulletPhysics
from src.utils import utils

class BodyType(IntEnum):
    static = 0
    kinematic = 1
    dynamic = 2

class PhysicsManager:
    def __init__(self):
        self.world = b2World(gravity=(0, 0), doSleep=True)
        self.collision_handler = CollisionHandler()
        self.time_step = 1.0 / 60
        self.tick = 0
        self.tanks_bodies = {}
        self.bullets_bodies = {}

    def update(self, entities_to_destroy):
        world_state = {"tanks":{}, "bullets":{}, "collisions":[]}
        try:
            self.cleanup_world(entities_to_destroy)            
            self.world.Step(self.time_step, 6, 2)
            for tank in list(self.tanks_bodies.values()):
                world_state["tanks"][tank.id] = tank.to_dict()
            for bullet in list(self.bullets_bodies.values()):
                world_state["bullets"][bullet.id] = bullet.to_dict()
            world_state["collisions"] = self.get_latest_collisions()
            self.tick += 1
                
            return world_state
        except Exception as e:
            utils.logger.warning(f"PhysicsManager update error: {e}")

    def create_body(self, body_type, position, fixture_def, **kwargs):
        return self.world.CreateBody(
            type=body_type,
            position=position,
            fixtures=fixture_def,
            **kwargs
        )

    def create_tank(self, id, position, dimentions, **kwargs):
        if id in self.tanks_bodies:
            raise ValueError(f"Tank with id {id} already exists.")
        body = self.create_body(
            body_type=BodyType.dynamic,
            position=position,
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=b2Vec2(dimentions) * 0.5), # * 0.5 because box2d uses half width and half height (almost went insane over this)
                density=2,
                friction=0.5,
                groupIndex=-id,
            ),
            **kwargs
        )
        tank_physics = TankPhysics(id, dimentions[0], dimentions[1], body)
        self.tanks_bodies[id] = tank_physics
    
    def create_bullet(self, id, position, angle, speed, radius=0.3, groupIndex=0, **kwargs):
        body = self.create_body(body_type=BodyType.dynamic,
                                                position=position,
                                                fixture_def=b2FixtureDef(
                                                    shape=b2CircleShape(radius=radius),
                                                    density=0.5,
                                                    friction=0,
                                                    restitution=1,
                                                    groupIndex = groupIndex
                                                ),
                                                bullet=True,
                                                linearVelocity=utils.get_linear_velocity(speed,angle),
                                                **kwargs
                                                )
        bullet_physics = BulletPhysics(id, body)
        self.bullets_bodies[id] = bullet_physics
    


    def handle_input(self, tank_id, input):
        tank = self.tanks_bodies.get(tank_id)
        if tank:
            tank.apply_input(input)      
            return      
        utils.logger.warning(f"Tank with id {tank_id} not found.")
    
    def destroy_body(self, body):
        self.world.DestroyBody(body)

    def cleanup_world(self, entities_to_destroy):
        for tank in entities_to_destroy["tanks"]:
            tank_body = self.tanks_bodies.get(tank)
            if tank_body:
                self.destroy_body(tank_body.body)
                del self.tanks_bodies[tank]
        for bullet in entities_to_destroy["bullets"]:
            bullet_body = self.bullets_bodies.get(bullet)
            if bullet_body:
                self.destroy_body(bullet_body.body)
                del self.bullets_bodies[bullet]

    def get_latest_collisions(self):
        contacts = self.world.contacts
        collisions = self.collision_handler.get_latest_collisions(contacts)
        return collisions