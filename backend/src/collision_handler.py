from src.tank import Tank
from src.bullet import Bullet

class CollisionHandler:
    
    def begin_contact_callback(self, bodyA, bodyB):
        if bodyA.userData is not None and bodyB.userData is not None:
            if isinstance(bodyA.userData, Tank) and isinstance(bodyB.userData, Tank):
                print("Tanks collided")
            elif isinstance(bodyA.userData, Tank) and isinstance(bodyB.userData, Bullet):
                print("Tank and bullet collided")
                bodyA.userData.health -= bodyB.userData.damage
                #bodyB.userData.isDead = True
            elif isinstance(bodyA.userData, Bullet) and isinstance(bodyB.userData, Tank):
                print("Bullet and tank collided")
                bodyB.userData.health -= bodyA.userData.damage
            elif isinstance(bodyA.userData, Bullet) and isinstance(bodyB.userData, Bullet):
                bodyA.userData.isDead = True
                bodyB.userData.isDead = True
                print("Bullets collided")
            else:
                print("Unknown collision")

    def end_contact_callback(self, bodyA, bodyB):
        pass