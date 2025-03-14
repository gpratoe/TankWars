from db.player_service import ps

class Player:
    def __init__(self, name:str, id=None, is_owner=False):
        self.id = id
        self.name = name
        self.validation_token = None # JWT token in a future
        self.game = None
        self.is_owner = is_owner
        self.color = None
        self.ready = False
        
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
        self.name = player['name']
        self.game = player['game']
        self.is_owner = player['is_owner']
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'is_owner': self.is_owner, 'color': self.color}