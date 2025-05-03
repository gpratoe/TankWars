from physics_manager import PhysicsManager, BodyType
from utils import utils
from Box2D import b2FixtureDef, b2PolygonShape

class Wall:
    def __init__(self, x, y, width, height, physics_manager: PhysicsManager):
        self.physics_manager = physics_manager
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.body = physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, 0)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((width/2, height/2))),
                density=0,
                friction=0
            ),
            userData=self
        )