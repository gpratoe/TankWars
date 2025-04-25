# Global game settings
GAME_WIDTH = 800
GAME_HEIGHT = 450

# Tank settings
TANK_WIDTH = 30
TANK_HEIGHT = 30
TANK_INITIAL_BULLETSPEED = 50
TANK_INITIAL_DAMAGE = 10

# Map settings
BOUNDRY_BLOCK_EDGE_WIDTH = GAME_WIDTH
BOUNDRY_BLOCK_EDGE_HEIGHT = 20

BOUNDRY_INLINE_EDGE_WIDTH = 20
BOUNDRY_INLINE_EDGE_HEIGHT = GAME_HEIGHT

BASES_TLEFT_BRIGHT_WIDTH = 20
BASES_TLEFT_BRIGHT_HEIGHT = TANK_HEIGHT * 2

BASES_BLEFT_TRIGHT_WIDTH = TANK_WIDTH * 2
BASES_BLEFT_TRIGHT_HEIGHT = 20

SETTINGS_JSON = { 
            'world': {
                'width': GAME_WIDTH,
                'height': GAME_HEIGHT,
            },
            'tank': {
                'width': TANK_WIDTH,
                'height': TANK_HEIGHT,
                'bullet_speed': TANK_INITIAL_BULLETSPEED,
                'damage': TANK_INITIAL_DAMAGE,
            }
        }