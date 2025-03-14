from pony.orm import Database, Required, Optional, PrimaryKey, Set
from db.settings import DATABASE_FILENAME


db = Database()

class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    game = Optional('Game', reverse='players')
    is_owner = Optional(bool, default=False)

class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    players = Set(Player)
    #state = Optional(Json) # probably won't be used since i don't need history of the game
    in_lobby = Optional(bool, default=True)
    max_players = Required(int)


db.bind(provider='sqlite', filename=DATABASE_FILENAME, create_db=True)

db.generate_mapping(create_tables=True)