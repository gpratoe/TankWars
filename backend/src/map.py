from src.physics_manager import PhysicsManager, BodyType
from src.utils import utils
from Box2D import b2FixtureDef, b2PolygonShape
from src.settings import *

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
                shape=b2PolygonShape(box=utils.vec2_to_world((self.w, BOUNDARIES_THICKNESS))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((BOUNDARIES_THICKNESS, self.h))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((self.w, BOUNDARIES_THICKNESS))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((self.w, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((BOUNDARIES_THICKNESS, self.h))),
                density=0,
                friction=0
            )
        )

        # need to make this:
        # --------------|----
        # |             |   |
        # |----         |   |
        # |                 |
        # |   |         ----|
        # |   |             |
        # ----|--------------

        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((BASES_TLEFT_X, BASES_TLEFT_Y)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((BASES_TLEFT_BRIGHT_WIDTH/2,
                                                              BASES_TLEFT_BRIGHT_HEIGHT/2))),
                density=0,
                friction=0
            )
        )

        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((BASES_BRIGHT_X, BASES_BRIGHT_Y)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((BASES_TLEFT_BRIGHT_WIDTH/2,
                                                              BASES_TLEFT_BRIGHT_HEIGHT/2))),
                density=0,
                friction=0
            )
        )

        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((BASES_TRIGHT_X, BASES_TRIGHT_Y)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((BASES_BLEFT_TRIGHT_WIDTH/2,
                                                              BASES_BLEFT_TRIGHT_HEIGHT/2))),
                density=0,
                friction=0
            )
        )

        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((BASES_BLEFT_X, BASES_BLEFT_Y)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((BASES_BLEFT_TRIGHT_WIDTH/2,
                                                              BASES_BLEFT_TRIGHT_HEIGHT/2))),
                density=0,
                friction=0
            )
        )
