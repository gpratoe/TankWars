from Box2D import b2ContactListener

class ContactListener(b2ContactListener):
    def __init__(self, colission_handler: callable):
        super().__init__()
        self.collision_handler = colission_handler

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        self.collision_handler(bodyA, bodyB)

            
    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body