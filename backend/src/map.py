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
        boundries_thickness = 20

        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, 0)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((self.w, boundries_thickness))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((boundries_thickness, self.h))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((0, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((self.w, boundries_thickness))),
                density=0,
                friction=0
            )
        )
        self.physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((self.w, self.h)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((boundries_thickness, self.h))),
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
        #
        # self.physics_manager.create_body(
        #     body_type=BodyType.static,
        #     position=utils.vec2_to_world((0, TANK_HEIGHT * 4)),
        #     fixture_def=b2FixtureDef(
        #         shape=b2PolygonShape(box=utils.vec2_to_world((100,
        #                                                       boundries_thickness))),
        #         density=0,
        #         friction=0
        #     )
        # )
       
        # self.physics_manager.create_body(
        #     body_type=BodyType.static,
        #     position=utils.vec2_to_world((self.w - BASES_TLEFT_BRIGHT_WIDTH,
        #                                   self.h - TANK_HEIGHT * 2)),
        #     fixture_def=b2FixtureDef(
        #         shape=b2PolygonShape(box=utils.vec2_to_world((BASES_TLEFT_BRIGHT_WIDTH,
        #                                                       BASES_TLEFT_BRIGHT_HEIGHT))),
        #         density=0,
        #         friction=0
        #     )
        # )