from src.physics_manager import PhysicsManager, BodyType
from src.utils import utils
from Box2D import b2FixtureDef, b2PolygonShape

class Map:
    def __init__(self, physics_manager: PhysicsManager, w=100, h=100):
        self.physics_manager = physics_manager
        self.w = w
        self.h = h
        self.create_boundaries()
    
    def create_boundaries(self):

        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, 0)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((self.w, 20))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((20, self.h))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((self.w, 20))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((self.w, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((20, self.h))),
                density=0,
                friction=0
            )
        )
       