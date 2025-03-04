from db.models import Player as PlayerModel, Game
from pony.orm import db_session, commit

class PlayerService:

    @db_session
    def create_player(self, name):
        if len(name) > 16:
            raise ValueError('Name must be 16 characters or less')
        player = PlayerModel(name=name)
        commit()
        return player.id
    
    @db_session
    def get_player(self, id):
        player = PlayerModel.get(id=id)
        if player is None:
            raise ValueError(f'Player with id {id} not found')
        return player.to_dict()

ps = PlayerService()