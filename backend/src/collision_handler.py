from enum import Enum

class CollisionType(Enum):
    BULLET = 1
    TANK = 2
    WALL = 3

class CollisionHandler:
    
    def begin_contact_callback(self, bodyA, bodyB):
        if bodyA.userData is None or bodyB.userData is None:
            return
        
        first = bodyA.userData
        second = bodyB.userData
        a_type = type(first).__name__
        b_type = type(second).__name__

        # Just so i dont have to duplicte cases
        if a_type < b_type:
            types = (a_type, b_type)
        else:
            types = (b_type, a_type)
            first, second = second, first
            
        
        match types:

            case ("Tank", "Tank"):
                pass
            
            case ("Bullet", "Tank"):
                second.health -= first.damage
                first.collided_with = CollisionType.TANK

            case ("Bullet", "Bullet"):
                first.collided_with = CollisionType.BULLET
                second.collided_with = CollisionType.BULLET

            case ("Bullet", "Wall"):
                first.collided_with = CollisionType.WALL

            case _:
                pass
    
    def end_contact_callback(self, bodyA, bodyB):
        pass