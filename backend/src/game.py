from Box2D import b2World
from src.utils import utils
from src.tank import Tank
from src.bullet import Bullet
from src.contactlistener import ContactListener
import json 
import asyncio


class Game:
    def __init__(self, w, h):
        self.w = utils.gameWidth = w
        self.h = utils.gameHeight = h
        self.world = utils.world = b2World(gravity=(0, 0), doSleep=True)
        self.world.contactListener = utils.cl = ContactListener(self.collision_handler)
        self.time_step = 1.0 / 60
        self.tanks = {}
        self.tanksw = 50
        self.tanksh = 25
        self.tank_initialpos = (self.w/2, self.h/2)
        self.bullets = {}
        self.prev_state = None


    def collision_handler(self, bodyA, bodyB):
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
                print("Bullets collided")
            else:
                print("Unknown collision")

    def add_tank(self, name):
        if self.tanks.get(name) is None:
            self.tanks[name] = Tank(name, self.tank_initialpos, self.tanksw, self.tanksh, 0, 10, 200)
            self.tanks[name].groupIndex = -self.tanks.__len__()
            self.bullets[name] = self.tanks[name].alive_bullets
            return 0
        else:
            return 1
        

        # maybe return 1 and 0 and handle the jsons in ws.py? idk
    def get_state(self):
        state = {
            "tanks": {name: tank.get_state() for name, tank in self.tanks.items()},
            "bullets": {name: [bullet.get_state() for bullet in bullets] for name, bullets in self.bullets.items()}
        }
        return state
    

    async def run(self):
        self.running = True
        while self.running:
            self.world.Step(self.time_step, 6, 0)
            for tank in self.tanks.values():
                tank.update()

            state = self.get_state()
            if state != self.prev_state:
                await utils.manager.broadcast(json.dumps({
                    "event": "state",
                    "data": self.get_state()
                }))
            self.prev_state = state

            await asyncio.sleep(self.time_step)

game = Game(1900, 1080)