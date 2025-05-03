from src.tank import Tank
from src.bullet import Bullet
from src.wall import Wall

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
                print("Tank and bullet collided")
                second.health -= first.damage
                first.isDead = True

            case ("Bullet", "Bullet"):
                first.isDead = True
                second.isDead = True
                print("Bullets collided")

            case ("Bullet", "Wall"):
                print("Bullet and wall collided")
                first.bounces_left -= 1

            case _:
                print("Unknown collision")
            
    def end_contact_callback(self, bodyA, bodyB):
        pass