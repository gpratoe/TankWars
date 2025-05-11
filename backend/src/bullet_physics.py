from src.collision_handler import EntityType
from Box2D import b2Body

class BulletPhysics:
    def __init__(self,id , body: b2Body):
        self.id = id
        self.body = body
        self.entity_type = EntityType.BULLET
        self.to_be_destroyed = False
        self.body.fixtures[0].userData = self

        
    def to_dict(self):
        return {
            'bulletx': self.body.position.x,
            'bullety': self.body.position.y,
            'angle': self.body.angle,
            'to_be_destroyed': self.to_be_destroyed,
        }        
