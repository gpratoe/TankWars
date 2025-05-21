# Global game settings
GAME_WIDTH = 800
GAME_HEIGHT = 450
UPDATE_RATE = 50 # ms

# Tank settings
TANK_WIDTH = 30
TANK_HEIGHT = 30
TANK_INITIAL_BULLETSPEED = 50
TANK_INITIAL_DAMAGE = 10

# Map settings
BOUNDARIES_THICKNESS = 20
BASES_SPACE = TANK_HEIGHT * 3

BASES_TLEFT_BRIGHT_WIDTH = 100
BASES_TLEFT_BRIGHT_HEIGHT = BOUNDARIES_THICKNESS

BASES_TLEFT_X = 0 + BOUNDARIES_THICKNESS + BASES_TLEFT_BRIGHT_WIDTH/2
BASES_TLEFT_Y = 0 + BOUNDARIES_THICKNESS + BASES_SPACE
BASES_BRIGHT_X = GAME_WIDTH - BOUNDARIES_THICKNESS - BASES_TLEFT_BRIGHT_WIDTH/2
BASES_BRIGHT_Y = GAME_HEIGHT - BOUNDARIES_THICKNESS - BASES_SPACE 

BASES_BLEFT_TRIGHT_WIDTH = BOUNDARIES_THICKNESS
BASES_BLEFT_TRIGHT_HEIGHT = 100

BASES_BLEFT_X = 0 + BOUNDARIES_THICKNESS + BASES_SPACE
BASES_BLEFT_Y = 0 + GAME_HEIGHT - BOUNDARIES_THICKNESS - BASES_BLEFT_TRIGHT_HEIGHT/2
BASES_TRIGHT_X = GAME_WIDTH - BOUNDARIES_THICKNESS - BASES_SPACE
BASES_TRIGHT_Y = 0 + BOUNDARIES_THICKNESS + BASES_BLEFT_TRIGHT_HEIGHT/2

SETTINGS_JSON = { 
            'world': {
                'width': GAME_WIDTH,
                'height': GAME_HEIGHT,
                'update_rate': UPDATE_RATE
            },
            'tank': {
                'width': TANK_WIDTH,
                'height': TANK_HEIGHT,
                'bullet_speed': TANK_INITIAL_BULLETSPEED,
                'damage': TANK_INITIAL_DAMAGE,
            },
            'map': {
                'boundaries_thickness': BOUNDARIES_THICKNESS,
                'bases_tleft_bright_width': BASES_TLEFT_BRIGHT_WIDTH,
                'bases_tleft_bright_height': BASES_TLEFT_BRIGHT_HEIGHT,
                'bases_bleft_tright_width': BASES_BLEFT_TRIGHT_WIDTH,
                'bases_bleft_tright_height': BASES_BLEFT_TRIGHT_HEIGHT,
                'bases_tleft_x': BASES_TLEFT_X,
                'bases_tleft_y': BASES_TLEFT_Y,
                'bases_bright_x': BASES_BRIGHT_X,
                'bases_bright_y': BASES_BRIGHT_Y,
                'bases_bleft_x': BASES_BLEFT_X,
                'bases_bleft_y': BASES_BLEFT_Y,
                'bases_tright_x': BASES_TRIGHT_X,
                'bases_tright_y': BASES_TRIGHT_Y,
            }
        }
