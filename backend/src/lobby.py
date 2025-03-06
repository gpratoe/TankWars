from db.game_service import gs
from src.player import Player
from src.utils import Utils
from fastapi import WebSocket
from pydantic import BaseModel
import json


class Lobby:
    ACTIVE_LOBBIES = {}

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
        
        self.websocket_url = Utils.API_URL + f'/game/{self.lobby_id}/ws'
        self.connections = {}

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
        cls.ACTIVE_LOBBIES[lobby.lobby_id] = lobby
        return game_dict

    
    @classmethod
    def from_db(cls, lobby_id):
        '''
        Use only for debbugging or handling data from past games.
        To get an active lobby use get_lobby() instead.
        '''
        lobby = cls(None, None, 2, lobby_id) # dummy values
        lobby.load_from_db()
        return lobby
    
    @classmethod
    def get_lobby(cls, lobby_id):
        '''
        Gets an active lobby from memory or pulls it from the db and set it as active.
        This method won't create a new lobby if it doesn't exist.
        '''
        lobby = cls.ACTIVE_LOBBIES.get(lobby_id)
        if not lobby:
            lobby = cls.from_db(lobby_id)
            cls.ACTIVE_LOBBIES[lobby_id] = lobby
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
        gs.remove_player_from_game(self.lobby_id, player_id)
        player = self.get_player(player_id)
        if player:
            self.__color_availability[player.color] = True
            self.players.remove(player)
        
        if self.connections.get(player_id):
            await self.connections[player_id].close()
            self.connections.pop(player_id)
        
        if len(self.players) > 0:
            self.load_from_db() # reload players and owner (if he left), use db as source of truth
            await self.broadcast({'event': 'player_left', 'player_id': player_id, 'owner': self.owner.id})

    async def connect_player(self, player_id: int, websocket: WebSocket):
        player = self.get_player(player_id)
        if not player:
            raise ValueError('Player not found in lobby')
        await websocket.accept()

        await self.broadcast({'event': 'player_joined', 'player': player.to_dict()})
        self.connections[player_id] = websocket

    async def disconnect_player(self, player_id: int):
        connection = self.connections.get(player_id)
        if connection:
            await connection.close()
            self.connections.pop(player_id)
        await self.broadcast({'event': 'player_dcd', 'player_id': player_id})

    async def broadcast(self, data: dict):
        try:
            for id, connection in self.connections.items():
                await connection.send_json(data)
        except Exception as e:
            print('Error broadcasting data', str(e))

    def get_players(self):
        players = [p.to_dict() for p in self.players]
        return players