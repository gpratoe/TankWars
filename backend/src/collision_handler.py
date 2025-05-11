from enum import Enum

class CollisionType(Enum):
    BULLET_TANK = 0
    TANK_TANK = 1
    BULLET_BULLET = 2
    BULLET_WALL = 3
    
class EntityType(Enum):
    BULLET = 0
    TANK = 1
    WALL = 2

class Collision:
    def __init__(self, first, second, type):
        self.first = first
        self.second = second
        self.type = type

class CollisionHandler:
    def __init__(self):
        pass
    
    def get_type(self, first, second):
        first_type = first.entity_type
        second_type = second.entity_type
        match (first_type, second_type):
            case (EntityType.TANK, EntityType.TANK):
                return CollisionType.TANK_TANK
            case (EntityType.BULLET, EntityType.TANK):
                return CollisionType.BULLET_TANK
            case (EntityType.TANK, EntityType.BULLET):
                return CollisionType.BULLET_TANK
            case (EntityType.BULLET, EntityType.BULLET):
                return CollisionType.BULLET_BULLET
            case (EntityType.BULLET, EntityType.WALL):
                return CollisionType.BULLET_WALL
            case (EntityType.WALL, EntityType.BULLET):
                return CollisionType.BULLET_WALL
            case _:
                pass
    def get_collision(self, first, second, ctype):
        fname = type(first).__name__
        sname = type(second).__name__
        if fname < sname:
            return Collision(first, second, ctype)
        return Collision(second,first, ctype)
    
    def get_latest_collisions(self, contacts):
        collisions = []
        for contact in contacts:
            fixtureA = contact.fixtureA
            fixtureB = contact.fixtureB
            if fixtureA.userData and fixtureB.userData:
                collision_type = self.get_type(fixtureA.userData, fixtureB.userData)
                if collision_type:
                    collision = self.get_collision(fixtureA.userData, fixtureB.userData, collision_type)
                    collisions.append(collision)
        return collisions
