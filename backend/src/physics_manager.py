from Box2D import b2World, b2FixtureDef, b2PolygonShape
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
        self.time_step = 1.0 / 60
        self.tick = 0

    
    def update(self):
        self.world.Step(self.time_step, 10, 3)
        self.tick += 1

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
    
    

    def destroy_body(self, body):
        self.world.DestroyBody(body)

