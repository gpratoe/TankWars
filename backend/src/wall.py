from src.collision_handler import EntityType

class Wall:
    '''
    Class representing a wall in the game.
    x and y are the coordinates of the center of the wall.
    '''
    def __init__(self, id, width, height, body):
        self.id = id
        self.width = width
        self.height = height
        self.entity_type = EntityType.WALL
        self.body = body
        self.body.fixtures[0].userData = self
