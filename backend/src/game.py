from Box2D import b2World
from src.utils import utils
from src.tank import Tank
from src.bullet import Bullet
from src.contactlistener import ContactListener
import json 
import asyncio
from src.settings import *
from src.entity_manager import EntityManager

class Game:
    def __init__(self, players, lobby_id, manager):
        self.w = GAME_WIDTH
        self.h = GAME_HEIGHT
        self.id = lobby_id
        self.players = players
        self.world = utils.world = b2World(gravity=(0, 0), doSleep=True)
        self.world.contactListener = utils.cl = ContactListener(self.collision_handler)
        self.time_step = 1.0 / 60
        self.tank_initialpos = (self.w/2, self.h/2)
        self.prev_state = None
        self.manager = manager
        self.entity_manager = EntityManager()


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
                bodyA.userData.isDead = True
                bodyB.userData.isDead = True
                print("Bullets collided")
            else:
                print("Unknown collision")
        

    
    def handle_data(self, data):
        if 'event' in data and 'payload' in data:
            event = data['event']
            payload = data['payload']
            if event == 'input':
                self.entity_manager.handle_client_input(payload)
        else:
            print("Invalid data received")


    def first_setup(self):
        for player in self.players:
            self.entity_manager.add_tank(player, self.tank_initialpos, 0)

    async def run(self):
        self.first_setup()
        self.running = True
        while self.running:
            self.world.Step(self.time_step, 10, 3)
            
            state = self.entity_manager.update()
            
            if state != self.prev_state:
                await self.manager.broadcast(json.dumps({
                    "event": "state",
                    "data": state
                }))
            self.prev_state = state

            await asyncio.sleep(self.time_step)