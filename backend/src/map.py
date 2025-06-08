from src.settings import *
from src.common_types import EntityType

class Map:
    def __init__(self, physics_manager, w=100, h=100):
        self.physics_manager = physics_manager
        self.w = w
        self.h = h
        self.id_counter = 0
        self.create_boundaries()
    
    def create_boundaries(self):

        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x= self.w/2,
            y= 0 + BOUNDARIES_THICKNESS/2,
            width= self.w,
            height= BOUNDARIES_THICKNESS,
        )
        self.id_counter += 1
        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x= BOUNDARIES_THICKNESS/2,
            y= self.h/2,
            width= BOUNDARIES_THICKNESS,
            height= self.h,
        )
        self.id_counter += 1
        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x = self.w - BOUNDARIES_THICKNESS/2,
            y = self.h/2,
            width= BOUNDARIES_THICKNESS,
            height= self.h,
        )
        self.id_counter += 1
        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x= self.w/2,
            y= self.h - BOUNDARIES_THICKNESS/2,
            width= self.w,
            height= BOUNDARIES_THICKNESS,
        )
        self.id_counter += 1
        # need to make this:
        # --------------|----
        # |             |   |
        # |----         |   |
        # |                 |
        # |   |         ----|
        # |   |             |
        # ----|--------------

        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x=BASES_TLEFT_X,
            y=BASES_TLEFT_Y,
            width=BASES_TLEFT_BRIGHT_WIDTH,
            height=BASES_TLEFT_BRIGHT_HEIGHT,
        )
        self.id_counter += 1
        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x=BASES_BRIGHT_X,
            y=BASES_BRIGHT_Y,
            width=BASES_TLEFT_BRIGHT_WIDTH,
            height=BASES_TLEFT_BRIGHT_HEIGHT,
        )
        self.id_counter += 1
        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x=BASES_BLEFT_X,
            y=BASES_BLEFT_Y,
            width=BASES_BLEFT_TRIGHT_WIDTH,
            height=BASES_BLEFT_TRIGHT_HEIGHT,
        )
        self.id_counter += 1
        self.physics_manager.create_body(
            type=EntityType.WALL,
            id=self.id_counter,
            x=BASES_TRIGHT_X,
            y=BASES_TRIGHT_Y,
            width=BASES_BLEFT_TRIGHT_WIDTH,
            height=BASES_BLEFT_TRIGHT_HEIGHT,
        )
        self.id_counter += 1
