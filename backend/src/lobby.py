from db.game_service import gs
from player import Player
from utils import Utils
from fastapi import WebSocket

colors = ["green", "blue", "yellow", "orange"]

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
        self.players = [owner]
        self.websocket_url = Utils.API_URL + f'/game/{self.lobby_id}/ws'
        self.connections = {}

    def create_db_entry(self):
        self.lobby_id = gs.create_game(self.name, self.max_players, self.owner.id)

    def load_from_db(self):
        if not self.lobby_id:
            raise ValueError('Lobby id not set')
        
        game = gs.get_game(self.lobby_id, include_players=True)
        self.name = game.name
        self.max_players = game.max_players
        self.players = [Player(p['name'], p['id']) for p in game.players]
        self.owner = self.players.filter(is_owner=True).first()

    @classmethod
    def new(cls, name: str, owner: Player, max_players: int):
        lobby = cls(name, owner, max_players)
        lobby.create_db_entry()
        cls.ACTIVE_LOBBIES[lobby.lobby_id] = lobby
        return

    
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

    async def connect_player(self, player_id: int, websocket: WebSocket):
        player = self.players.filter(id=player_id).first()
        if not player:
            raise ValueError('Player not found in lobby')
        await websocket.accept()
        self.connections[player_id] = websocket

    async def disconnect_player(self, player_id: int):
        player = self.players.filter(id=player_id).first()
        if not player:
            raise ValueError('Player not found in lobby')
        connection = self.connections.get(player_id)
        if connection:
            connection.close()
            self.connections[player_id] = None

    def add_player(self, player: Player):
        gs.add_player_to_game(self.lobby_id, player.id)
        self.players.append(player)

    def remove_player(self, player: Player):
        gs.remove_player_from_game(self.lobby_id, player.id)
        self.load_from_db() # reload players and owner (if he left), use db as source of truth