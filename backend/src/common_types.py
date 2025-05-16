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

    def __eq__(self, other):
        if not isinstance(other, Collision):
            return False
        return (
            self.first == other.first and
            self.second == other.second and
            self.type == other.type
        )
    def __hash__(self):
        return hash((frozenset({id(self.first), id(self.second)}), self.type))


