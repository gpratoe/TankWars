import math
import asyncio
from src.settings import *
from src.entity_manager import EntityManager
from api.ws import ConnectionManager
from src.physics_manager import PhysicsManager
from src.map import Map

class Game:
    def __init__(self, players, lobby_id, connection_manager: ConnectionManager,
                 entity_manager: EntityManager, physics_manager: PhysicsManager):
        self.w = GAME_WIDTH
        self.h = GAME_HEIGHT
        self.id = lobby_id
        self.players = players
        self.prev_state = None
        self.connection_manager = connection_manager
        self.physics_manager = physics_manager
        self.entity_manager = entity_manager
        

    
    async def handle_data(self, data, player_id):
        if 'event' in data and 'payload' in data:
            event = data['event']
            payload = data['payload']
            if event == 'input':
                self.entity_manager.handle_client_input(payload, player_id)
        else:
            print("Invalid data received")


    async def first_setup(self):
        middle = (self.w/2, self.h/2)
        self.map = Map(self.physics_manager, self.w, self.h)
        
        corners = [(TANK_WIDTH + BOUNDARIES_THICKNESS, TANK_HEIGHT + BOUNDARIES_THICKNESS),
                    (self.w - TANK_WIDTH - BOUNDARIES_THICKNESS, self.h - TANK_HEIGHT - BOUNDARIES_THICKNESS),
                    (self.w - TANK_WIDTH - BOUNDARIES_THICKNESS, 0 + TANK_HEIGHT + BOUNDARIES_THICKNESS),
                    (0 + TANK_WIDTH + BOUNDARIES_THICKNESS, self.h - TANK_HEIGHT - BOUNDARIES_THICKNESS)]
        
        angles = [math.degrees(math.atan2(middle[1] - corner[1], middle[0] - corner[0])) for corner in corners]

        for player in self.players:
            pos = corners.pop(0)
            angle = angles.pop(0)
            self.entity_manager.add_tank(player, pos, angle)



    async def broadcast(self, data):
        await self.connection_manager.broadcast(data, self.id)

    async def run(self):
        
        self.running = True
        while self.running:
            self.physics_manager.update()
            
            if self.physics_manager.tick % 3 == 0:
                state = self.entity_manager.update()
                if state and state != self.prev_state:
                    await self.broadcast({
                        "event": "state",
                        "payload": state
                    })
                    self.prev_state = state

            await asyncio.sleep(self.physics_manager.time_step)