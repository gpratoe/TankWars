from db.player_service import ps
from fastapi import WebSocket

class Player:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
        self.validation_token = None # JWT token in a future
        self.game = None
        self.ws = {} # Active Websocket connections (lobby, game, chat, etc.)
        
        if not self.id: # Creates entry or retrieves from db if id is provided
            self.create_db_entry()
        else:
            self.load_from_db()
    
    def create_db_entry(self):
        self.id = ps.create_player(self.name)

    def load_from_db(self):
        if not self.id:
            raise ValueError('Player id not set')
        
        player = ps.get_player(self.id)
        self.name = player.name
        self.game = player.game