from concurrent.futures import ThreadPoolExecutor
import math
import asyncio
from src.light_physics_manager import LP_PhysicsManager
from src.settings import *
from src.entity_manager import EntityManager
from api.ws import ConnectionManager
from src.map import Map
from src.utils import utils
import time
from src.mediator import LogicPhysicsMediator
from src.input_router import InputRouter

class Game:
    def __init__(self, players, lobby_id, connection_manager: ConnectionManager):
        self.w = GAME_WIDTH
        self.h = GAME_HEIGHT
        self.id = lobby_id
        self.players = players
        self.prev_state = None
        self.connection_manager = connection_manager
        self.input_router = InputRouter()
        self.physics_manager = LP_PhysicsManager()
        self.entity_manager = EntityManager()
        self.logic_physics_mediator = LogicPhysicsMediator(self.physics_manager, self.entity_manager, self.input_router)
        self.physics_manager.collision_handler.set_mediator(self.logic_physics_mediator)
        self.latest_inputs = {}
        self.entities_to_destroy = {"tanks":[], "bullets":[]}
        self.latest_collisions = None
        self.executor = ThreadPoolExecutor(max_workers=1)

    async def handle_disconnect(self, player_id):
        player = next(filter(lambda p : p.id == player_id, self.players))

        if player in self.players:
            self.players.remove(player)
            await self.connection_manager.disconnect(player_id)
            if len(self.players) == 0:
                self.running = False
                utils.logger.info(f"stoping loop for game: {self.id} as all players disconnected")
                return
            else:
                await self.broadcast({
                    "event": "player_dcd",
                    "payload": {"player_id": player_id}
                })
        else:
            utils.logger.info(f"Player {player_id} not found in players list")
    
    async def handle_data(self, data, player_id):
        if 'event' in data and 'payload' in data:
            event = data['event']
            payload = data['payload']
            if event == 'input':
                self.latest_inputs[player_id] = payload
        else:
            utils.logger.info("Invalid data received")


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
        await self.connection_manager.broadcast(data)

    def apply_inputs(self):
        for player_id, input in self.latest_inputs.items():
            self.input_router.handle_input(input, player_id)
    
    async def run(self):
        
        self.running = True
        while self.running:
            start = time.perf_counter()
            
            self.apply_inputs()
            t0 = time.perf_counter()

            try:
                await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(
                        self.executor,
                        self.physics_manager.update
                    ),
                    timeout=0.1
                )
            except asyncio.TimeoutError:
                utils.logger.info("PhysicsManager update timed out")
                continue
            t1 = time.perf_counter()

            if self.physics_manager.tick % 3 == 0:
                state = self.entity_manager.get_last_state()
                if state and state != self.prev_state:
                    await self.broadcast({
                        "event": "state",
                        "payload": state
                    })
                    self.prev_state = state

            end = time.perf_counter()
            #print(f"Physics: {(t1 - t0)*1000:.3f} ms, Total: {(end - start)*1000:.3f} ms")

            await asyncio.sleep(self.physics_manager.time_step)

        utils.logger.info("Game loop stopped")
