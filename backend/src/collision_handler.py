from src.tank import Tank
from src.bullet import Bullet
from src.wall import Wall

class CollisionHandler:
    
    def begin_contact_callback(self, bodyA, bodyB):
        if bodyA.userData is not None and bodyB.userData is not None:
            a_data = bodyA.userData
            b_data = bodyB.userData
            types = (type(a_data).__name__, type(b_data).__name__)
            
            match types:
                
                case ("Tank", "Tank"):
                    print("Tanks collided")

                case ("Tank", "Bullet"):
                    print("Tank and bullet collided")
                    bodyA.userData.health -= bodyB.userData.damage
                    bodyB.userData.isDead = True

                case ("Bullet", "Tank"):
                    print("Bullet and tank collided")
                    bodyB.userData.health -= bodyA.userData.damage

                case ("Bullet", "Bullet"):
                    bodyA.userData.isDead = True
                    bodyB.userData.isDead = True
                    print("Bullets collided")

                case ("Wall", "Bullet"):
                    print("Bullet and wall collided")
                    bodyB.userData.isDead = True

                case ("Bullet", "Wall"):
                    print("Bullet and wall collided")
                    bodyA.userData.isDead = True

                case _:
                    print("Unknown collision")
            
    def end_contact_callback(self, bodyA, bodyB):
        pass