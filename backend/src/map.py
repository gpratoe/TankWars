from src.physics_manager import PhysicsManager, BodyType
from src.utils import utils
from Box2D import b2FixtureDef, b2PolygonShape
from src.settings import *
from wall import Wall

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

        Wall(
            x=utils.to_pixel(BASES_TLEFT_X),
            y=utils.to_pixel(BASES_TLEFT_Y),
            width=utils.to_pixel(BASES_TLEFT_BRIGHT_WIDTH),
            height=utils.to_pixel(BASES_TLEFT_BRIGHT_HEIGHT),
            physics_manager=self.physics_manager
        )
        Wall(
            x=utils.to_pixel(BASES_BRIGHT_X),
            y=utils.to_pixel(BASES_BRIGHT_Y),
            width=utils.to_pixel(BASES_BLEFT_TRIGHT_WIDTH),
            height=utils.to_pixel(BASES_BLEFT_TRIGHT_HEIGHT),
            physics_manager=self.physics_manager
        )
        Wall(
            x=utils.to_pixel(BASES_BLEFT_X),
            y=utils.to_pixel(BASES_BLEFT_Y),
            width=utils.to_pixel(BASES_BLEFT_TRIGHT_WIDTH),
            height=utils.to_pixel(BASES_BLEFT_TRIGHT_HEIGHT),
            physics_manager=self.physics_manager
        )
        Wall(
            x=utils.to_pixel(BASES_BLEFT_X),
            y=utils.to_pixel(BASES_BLEFT_Y),
            width=utils.to_pixel(BASES_BLEFT_TRIGHT_WIDTH),
            height=utils.to_pixel(BASES_BLEFT_TRIGHT_HEIGHT),
            physics_manager=self.physics_manager
        )