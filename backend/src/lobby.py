from db.game_service import gs
from player import Player


colors = ["green", "blue", "yellow", "orange"]
# thinking of creating the db entry first and then creating the object, so the id is already set
# and the object can be used to update the db entry

# or maybe i just create the db entry on the __init__ method
# and then just update the object with the id

class Lobby:
    def __init__(self, name: str, owner: (Player | None), max_players: int, id: (int | None) = None):
        self.lobby_id = id # lobby/game id will be the same
        self.max_players = max_players
        self.name = name
        self.owner = owner
        self.players = [owner]
        self.websocket_url = None # Maybe later this is filled with a generated url based on the lobby id 

        if not self.lobby_id:
            self.create_db_entry()
        else:
            self.load_from_db()


    def create_db_entry(self):
        self.lobby_id = gs.create_game(self.name, self.max_players, self.owner.id)

    def load_from_db(self):
        if not self.lobby_id:
            raise ValueError('Lobby id not set')
        
        game = gs.get_game(self.lobby_id, include_players=True)
        self.name = game.name
        self.max_players = game.max_players
        self.players = [Player(p.name, p.id) for p in game.players]
        self.owner = self.players.filter(is_owner=True).first()

    def add_player(self, player: Player):
        gs.add_player_to_game(self.lobby_id, player.id)
        self.players.append(player)