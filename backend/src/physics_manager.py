from Box2D import b2World
from src.contactlistener import ContactListener
from enum import IntEnum

class BodyType(IntEnum):
    static = 0
    kinematic = 1
    dynamic = 2

class PhysicsManager:
    def __init__(self, begin_contact_callback: callable):
        self.world = b2World(gravity=(0, 0), doSleep=True)
        self.world.contactListener = ContactListener(begin_contact_callback)
        self.time_step = 1.0 / 60

    
    def update(self):
        self.world.Step(self.time_step, 10, 3)

    def create_body(self, body_type, position, fixture_def, **kwargs):
        return self.world.CreateBody(
            type=body_type,
            position=position,
            fixtures=fixture_def,
            **kwargs
        )

    def destroy_body(self, body):
        self.world.DestroyBody(body)

