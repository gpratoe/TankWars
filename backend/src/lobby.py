from db.game_service import gs
from src.player import Player
from fastapi import WebSocket
from src.game import Game
import asyncio
from api.ws import ConnectionManager
import time
from src.settings import *
from src.utils import utils
from src.game_state_machine import GameStateMachine

class Lobby:

    def __init__(self, name: (str | None), owner: (Player | None),
                  max_players: int, id: (int | None) = None):
        
        if max_players < 2 or max_players > 4:
            raise ValueError('Max players must be between 2 and 4')
        self.max_players = max_players
        self.lobby_id = id # lobby/game id will be the same
        self.name = name
        self.owner = owner
        self.players = []
        self.__color_availability = {'green': True, 'blue': True, 'yellow': True, 'orange': True} 
        if owner:
            self.players = [owner]
            owner.color = self.__find_color()

        self.manager = None
        self.game = None

    def create_db_entry(self):
        game = gs.create_game(self.name, self.max_players, self.owner.id).to_dict()
        self.lobby_id = game['id']
        return game

    def load_from_db(self):
        if not self.lobby_id:
            raise ValueError('Lobby id not set')
        
        game = gs.get_game(self.lobby_id, include_players=True)
        self.name = game['name']
        self.max_players = game['max_players']
        new_players = [Player(p['name'], p['id']) for p in game['players']]
        

        for player in new_players:
            existing_player = self.get_player(player.id)
            if existing_player and existing_player.color:
                player.color = existing_player.color
            else:
                player.color = self.__find_color()

        self.players = new_players
        self.owner = None
        for player in self.players:
            if player.is_owner:
                self.owner = player
                break


    def __find_color(self):
        for color, available in self.__color_availability.items():
            if available:
                self.__color_availability[color] = False
                return color

    @classmethod
    def new(cls, name: str, owner: Player, max_players: int):
        lobby = cls(name, owner, max_players)
        game_dict = lobby.create_db_entry()
        lobby.manager = ConnectionManager(lobby.lobby_id)
        return lobby, game_dict

    
    @classmethod
    def from_db(cls, lobby_id):
        '''
        Use only for debbugging or handling data from past games.
        '''
        lobby = cls(None, None, 2, lobby_id) # dummy values
        lobby.load_from_db()
        return lobby
    

    def add_player(self, player: Player):
        gs.add_player_to_game(self.lobby_id, player.id)
        self.players.append(player)
        player.color = self.__find_color()
        return {'color': player.color}
    
    def get_player(self, player_id: int):
        for player in self.players:
            if player.id == player_id:
                return player
        return None

    async def remove_player(self, player_id: int):
        player = self.get_player(player_id)
        if not player:
            return
        gs.remove_player_from_game(self.lobby_id, player_id)
        if player:
            self.__color_availability[player.color] = True
            self.players.remove(player)

        if len(self.players) > 0:
            self.load_from_db() # reload players and owner (if he left), use db as source of truth
            await self.broadcast({'event': 'player_left', 'player_id': player_id, 'owner': self.owner.id})

    async def connect_player(self, player_id: int, websocket: WebSocket):
        player = self.get_player(player_id)
        if not player:
            raise ValueError('Player not found in lobby')

        await self.broadcast({'event': 'player_joined', 'player': player.to_dict()})
        await self.manager.connect(websocket, player_id)

    async def disconnect_player(self, player_id: int):
        await self.manager.disconnect(player_id)
        await self.remove_player(player_id)
        await self.broadcast({'event': 'player_dcd', 'player_id': player_id})

    async def broadcast(self, data: dict):
        await self.manager.broadcast(data)

    def get_players(self):
        players = [p.to_dict() for p in self.players]
        return players
    
    async def handle_data(self, data: dict, player_id: int):
        if 'event' not in data or 'payload' not in data:
            return
        event = data['event']
        payload = data['payload']
        if event == 'chat_msg':
            msg = payload['msg']
            await self.handle_chat_msg(msg, player_id)

    async def handle_chat_msg(self, msg: str, sender_id: int):
        sender = self.get_player(sender_id)
        current_time = time.strftime('%H:%M', time.localtime())
        data = {'event': 'chat_msg',
                'payload': {'msg': msg, 
                            'sender': sender.name, 
                            'sender_id': sender_id, 
                            'time': current_time
                            }
                }
        await self.broadcast(data)

    
    async def start_game(self, owner_id: int):
        if owner_id != self.owner.id:
            raise ValueError('Only the owner can start the game')
        
        resp = gs.start_game(self.lobby_id, owner_id)
        gsm = GameStateMachine.get_gsm(self.lobby_id)
        
        self.game = Game(players=self.players,
                         lobby_id=self.lobby_id,
                         connection_manager=self.manager,
                         gsm=gsm,
                    )   

        game_settings = SETTINGS_JSON

        await self.broadcast({'event': 'game_settings',
                               'payload': game_settings})
        utils.logger.info(f"llamando game run para el lobby: {self.lobby_id}")
        asyncio.create_task(self.game.run())

        await self.broadcast({'event': 'game_started'})

        return resp
