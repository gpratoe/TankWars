'''
    This module defines the high-level game flow states a player can be in during the web game 
(e.g., lobby, game setup, countdown, in-game, etc).
    It is unrelated to the gameplay state updates exchanged during a match, such as tank or bullet positions,
velocities, or other real-time entity data.

    Dependencies could be clearer, the main purpose of this was to have specific points to setup data and configuration
based on diferent key-points in the game flow. But i found it useful to also use it as a some kind of "router" for the data.
'''
from enum import Enum
from abc import ABC, abstractmethod
import time
import asyncio
from src.lobby import Lobby

class GameState(Enum):
    LOBBY = "lobby"
    PREV_GAME_CONFIG = "prev_game_config"
    COUNTDOWN = "countdown"
    IN_GAME = "in_game"
    GAME_OVER = "game_over"


class State(ABC):
    @abstractmethod
    async def handle_data(self, data: dict, player_id: int):
        pass

    @abstractmethod
    async def enter(self):
        pass

    @abstractmethod
    async def exit(self):
        pass

class GameStateMachine:
    ACTIVE_GSM = {}

    def __init__(self, lobby: (Lobby | None)):
        self.lobby = lobby
        self.states = {
            GameState.LOBBY: LobbyState(self),
            GameState.PREV_GAME_CONFIG: PrevGameConfigState(self),
            GameState.COUNTDOWN: CountdownState(self),
            GameState.IN_GAME: InGameState(self),
            GameState.GAME_OVER: None,
        }
        self.current_state = self.states[GameState.LOBBY]
    
    async def handle_data(self, data: dict, player_id: int):
        await self.current_state.handle_data(data, player_id)

    async def change_state(self, new_state: GameState):
        if self.current_state:
            await self.current_state.exit()
        self.current_state = self.states[new_state]
        await self.current_state.enter()

    async def start_game(self, owner_id: int):
        if not self.lobby:
            raise ValueError('Lobby not set in GameStateMachine')
        resp = await self.lobby.start_game(owner_id)
        await self.change_state(GameState.PREV_GAME_CONFIG)
        return resp

    @classmethod
    def new(cls, lobby):
        gsm = cls(lobby)
        cls.ACTIVE_GSM[lobby.lobby_id] = gsm

    @classmethod
    def get_gsm(cls, lobby_id):
        gsm = cls.ACTIVE_GSM.get(lobby_id)
        if gsm is None:
            raise ValueError(f'GameStateMachine with id {lobby_id} not found')
        return gsm


class LobbyState(State):
    '''
    Represents the time before the game starts, where players cand join and chat.
    '''
    def __init__(self, game_state_machine):
        self.game_state_machine = game_state_machine
        self.lobby = game_state_machine.lobby

    async def handle_data(self, data: dict, player_id: int):
        await self.lobby.handle_data(data, player_id)

    async def enter(self):
        pass

    async def exit(self):
        pass

class PrevGameConfigState(State):
    '''
    Represents an in-between state where we left the lobby, but the game is not fully configured yet. Here we 
    create the first state of the game, that is, the tanks initial positions and such.
    It also takes care of player synchronization, so we make sure that all players are "ready" before starting the
    initial coundown and actually starting the game.
    '''
    def __init__(self, game_state_machine):
        self.game_state_machine = game_state_machine
        self.lobby = game_state_machine.lobby
        self.game = self.lobby.game
        self.first_state = {}
    
    async def handle_data(self, data: dict, player_id: int):
        if 'event' not in data or 'payload' not in data:
            return
        
        event = data['event']
        payload = data['payload']
        
        match event:
            case 'chat_msg':
                msg = payload['msg']
                await self.lobby.handle_chat_msg(msg, player_id)
            
            case 'player_ready':
                player = self.lobby.get_player(player_id)
                if player:
                    player.ready = True
                    await self.game.connection_manager.send_message(self.first_state, self.game.id, player_id)

                    all_ready = all(p.ready for p in self.lobby.players)
                    if all_ready:
                        await self.game_state_machine.change_state(GameState.COUNTDOWN)
            
            case _:
                pass


    async def enter(self):
        self.game = self.lobby.game
        if not self.game:
            raise Exception("Game not found in PrevGameConfigState")
    
        await self.game.first_setup()
        self.first_state = {
                'event': 'init_game',
                'payload': {'tanks':{t.id: t.get_state()[0] for t in self.game.entity_manager.tanks.values()}}
            }
        
    async def exit(self):
        pass
        
            

class CountdownState(State):
    '''
    Just a countdown before game starts.
    '''
    def __init__(self, game_state_machine):
        self.game_state_machine = game_state_machine
        self.lobby = game_state_machine.lobby
        self.game = self.lobby.game
        self.countdown_seconds = 3

    async def handle_data(self, data: dict, player_id: int):
        if 'event' not in data or 'payload' not in data:
            return
        event = data['event']
        payload = data['payload']

        if event == 'chat_msg':
            msg = payload['msg']
            await self.lobby.handle_chat_msg(msg, player_id)

    async def enter(self):
        self.game = self.lobby.game
        if not self.game:
            raise Exception("Game not found in CountdownState")
        
        now = time.time() * 1000
        countdown_ms = self.countdown_seconds * 1000
        countdown_event = {
            'event': 'countdown',
            'payload': {'countdown_ms': countdown_ms,
                        'timestamp': now}
        }
        await self.game.connection_manager.broadcast(countdown_event, self.game.id)

        await asyncio.sleep(self.countdown_seconds)
        await self.game_state_machine.change_state(GameState.IN_GAME)
    


    async def exit(self):
        pass


class InGameState(State):
    '''
    Represents the in-game state, where players can move, shoot, etc.
    '''
    def __init__(self, game_state_machine):
        self.game_state_machine = game_state_machine
        self.lobby = game_state_machine.lobby
        self.game = self.lobby.game

    async def handle_data(self, data: dict, player_id: int):
        if 'event' not in data or 'payload' not in data:
            return
        
        event = data['event']
        payload = data['payload']
        
        if event == 'chat_msg':
                msg = payload['msg']
                await self.lobby.handle_chat_msg(msg, player_id)
        else:
            await self.game.handle_data(data, player_id)
    
    async def enter(self):
        self.game = self.lobby.game
        if not self.game:
            raise Exception("Game not found in InGameState")
        pass
    async def exit(self):
        pass