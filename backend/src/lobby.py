from db.game_service import gs
from player import Player


colors = ["green", "blue", "yellow", "orange"]

class Lobby:

    def __init__(self, name: (str | None), owner: (Player | None),
                  max_players: int, id: (int | None) = None):
        
        if max_players < 2 or max_players > 4:
            raise ValueError('Max players must be between 2 and 4')
        
        self.max_players = max_players
        self.lobby_id = id # lobby/game id will be the same
        self.name = name
        self.owner = owner
        self.players = [owner]
        self.websocket_url = None # Maybe later this is filled with a generated url based on the lobby id 

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
        return

    @classmethod
    def from_db(cls, lobby_id):
        lobby = cls(None, None, 2, lobby_id) # dummy values
        lobby.load_from_db()
        return lobby

    def add_player(self, player: Player):
        gs.add_player_to_game(self.lobby_id, player.id)
        self.players.append(player)

    def remove_player(self, player: Player):
        gs.remove_player_from_game(self.lobby_id, player.id)
        self.players.remove(player)