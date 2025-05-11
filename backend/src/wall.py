from src.physics_manager import PhysicsManager, BodyType
from src.utils import utils
from Box2D import b2FixtureDef, b2PolygonShape
from src.collision_handler import EntityType

class Wall:
    '''
    Class representing a wall in the game.
    x and y are the coordinates of the center of the wall.
    '''
    def __init__(self, x, y, width, height, physics_manager: PhysicsManager):
        self.physics_manager = physics_manager
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.entity_type = EntityType.WALL
        
        self.body = physics_manager.create_body(
            body_type=BodyType.static,
            position=utils.vec2_to_world((x, y)),
            fixture_def=b2FixtureDef(
                shape=b2PolygonShape(box=utils.vec2_to_world((width/2, height/2))),
                density=0,
                friction=0,
                userData=self,
            ),
        )