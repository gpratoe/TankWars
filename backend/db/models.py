from pony.orm import Database, Required, Optional, PrimaryKey, Set, Json
from db.settings import DATABASE_FILENAME


db = Database()

class Player(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    color = Optional(str)
    game = Optional('Game', reverse='players')

class Game(db.Entity):
    id = PrimaryKey(int, auto=True)
    players = Set(Player)
    state = Required(Json)
    lobby = Optional(int)   


db.bind(provider='sqlite', filename=DATABASE_FILENAME, create_db=True)

db.generate_mapping(create_tables=True)