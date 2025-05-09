from Box2D import b2World, b2FixtureDef, b2PolygonShape, b2CircleShape
from src.contactlistener import ContactListener
from enum import IntEnum
from src.collision_handler import CollisionHandler
from src.utils import utils

class BodyType(IntEnum):
    static = 0
    kinematic = 1
    dynamic = 2

class PhysicsManager:
    def __init__(self):
        self.world = b2World(gravity=(0, 0), doSleep=True)
        self.world.contactListener = ContactListener(CollisionHandler())
        self.entity_manager = None
        self.time_step = 1.0 / 60
        self.tick = 0

    
    def update(self):
        try:
            for tank in self.entity_manager.tanks.values():
                tank.update_physics()
            self.world.Step(self.time_step, 10, 3)
            self.tick += 1
            self.cleanup_world()
        except Exception as e:
            print(f"PhysicsManager update error: {e}")

    def create_body(self, body_type, position, fixture_def, **kwargs):
        return self.world.CreateBody(
            type=body_type,
            position=position,
            fixtures=fixture_def,
            **kwargs
        )

    def create_tank(self, position, dimentions, groupIndex=0, **kwargs):
        return self.create_body(
            body_type=BodyType.dynamic,
            position=position,
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world(dimentions * 0.5)), # * 0.5 because box2d uses half width and half height (almost went insane over this)
                density=2,
                friction=0.5,
                groupIndex=groupIndex 
            ),
            **kwargs
        )
    
    def create_bullet(self, position, direction, speed, radius=3, groupIndex=0, **kwargs):
        return self.create_body(body_type=BodyType.dynamic,
                                                position=utils.vec2_to_world(position),
                                                fixture_def=b2FixtureDef(
                                                    shape=b2CircleShape(radius=utils.to_world(radius)),
                                                    density=0.5,
                                                    friction=0,
                                                    restitution=1,
                                                    groupIndex = groupIndex
                                                ),
                                                bullet=True,
                                                linearVelocity=(speed * direction[0], speed * direction[1]),
                                                **kwargs
                                                )
    

    def destroy_body(self, body):
        self.world.DestroyBody(body)

    def cleanup_world(self):
        for body in self.world.bodies:
            if body.userData and hasattr(body.userData, 'is_dead') and body.userData.is_dead:
                self.destroy_body(body)

