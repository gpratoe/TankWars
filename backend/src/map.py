from src.physics_manager import PhysicsManager
from src.settings import *
from src.wall import Wall

class Map:
    def __init__(self, physics_manager: PhysicsManager, w=100, h=100):
        self.physics_manager = physics_manager
        self.w = w
        self.h = h
        self.create_boundaries()
    
    def create_boundaries(self):

        Wall(
            x= self.w/2,
            y= 0 + BOUNDARIES_THICKNESS/2,
            width= self.w,
            height= BOUNDARIES_THICKNESS,
            physics_manager=self.physics_manager
        )
        Wall(
            x= BOUNDARIES_THICKNESS/2,
            y= self.h/2,
            width= BOUNDARIES_THICKNESS,
            height= self.h,
            physics_manager=self.physics_manager
        )
        Wall(
            x = self.w - BOUNDARIES_THICKNESS/2,
            y = self.h/2,
            width= BOUNDARIES_THICKNESS,
            height= self.h,
            physics_manager=self.physics_manager
        )
        Wall(
            x= self.w/2,
            y= self.h - BOUNDARIES_THICKNESS/2,
            width= self.w,
            height= BOUNDARIES_THICKNESS,
            physics_manager=self.physics_manager
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
            x=BASES_TLEFT_X,
            y=BASES_TLEFT_Y,
            width=BASES_TLEFT_BRIGHT_WIDTH,
            height=BASES_TLEFT_BRIGHT_HEIGHT,
            physics_manager=self.physics_manager
        )
        Wall(
            x=BASES_BRIGHT_X,
            y=BASES_BRIGHT_Y,
            width=BASES_TLEFT_BRIGHT_WIDTH,
            height=BASES_TLEFT_BRIGHT_HEIGHT,
            physics_manager=self.physics_manager
        )
        Wall(
            x=BASES_BLEFT_X,
            y=BASES_BLEFT_Y,
            width=BASES_BLEFT_TRIGHT_WIDTH,
            height=BASES_BLEFT_TRIGHT_HEIGHT,
            physics_manager=self.physics_manager
        )
        Wall(
            x=BASES_TRIGHT_X,
            y=BASES_TRIGHT_Y,
            width=BASES_BLEFT_TRIGHT_WIDTH,
            height=BASES_BLEFT_TRIGHT_HEIGHT,
            physics_manager=self.physics_manager
        )