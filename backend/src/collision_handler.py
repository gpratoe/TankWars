from enum import Enum

class CollisionType(Enum):
    BULLET_TANK = 0
    TANK_TANK = 1
    BULLET_BULLET = 2
    BULLET_WALL = 3
    

class Collision:
    def __init__(self, first, second, type):
        self.first = first
        self.second = second
        self.type = type

class CollisionHandler:
    def __init__(self):
        self.latest_collisions = []
    
    def clear_collisions(self):
        self.latest_collisions = []

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
            case ("TankPhysics", "TankPhysics"):
                pass
            
            case ("BulletPhysics", "TankPhysics"):
                self.latest_collisions.append(Collision(first, second, CollisionType.BULLET_TANK))

            case ("BulletPhysics", "BulletPhysics"):
                self.latest_collisions.append(Collision(first, second, CollisionType.BULLET_BULLET))

            case ("BulletPhysics", "Wall"):
                self.latest_collisions.append(Collision(first, second, CollisionType.BULLET_WALL))
            case _:
                pass
       
    def end_contact_callback(self, bodyA, bodyB):
        pass