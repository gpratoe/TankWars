from Box2D import b2ContactListener
from src.collision_handler import CollisionHandler

class ContactListener(b2ContactListener):
    def __init__(self, colission_handler: CollisionHandler):
        super().__init__()
        self.collision_handler = colission_handler

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        self.collision_handler.begin_contact_callback(bodyA, bodyB)

            
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        self.collision_handler.end_contact_callback(bodyA, bodyB)