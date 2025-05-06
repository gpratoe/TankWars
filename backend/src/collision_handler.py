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
                print("Tanks collided")

            case ("Bullet", "Tank"):
                second.health -= first.damage
                first.collided_with = CollisionType.TANK
                print("Tank and bullet collided")

            case ("Bullet", "Bullet"):
                first.collided_with = CollisionType.BULLET
                second.collided_with = CollisionType.BULLET
                print("Bullets collided")

            case ("Bullet", "Wall"):
                first.collided_with = CollisionType.WALL
                print("Bullet and wall collided")

            case _:
                print("Unknown collision")
            
    def end_contact_callback(self, bodyA, bodyB):
        pass