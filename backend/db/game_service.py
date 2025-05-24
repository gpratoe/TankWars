from db.models import Player, Game
from pony.orm import db_session

class GameService:

    @db_session
    def create_game(self, name, max_players, owner_id):
        if max_players < 2 or max_players > 4:
            raise ValueError('Max players must be between 2 and 4')
        if len(name) > 16:
            raise ValueError('Name must be 16 characters or less')
        
        player = Player.get(id=owner_id)
        
        if player is None:
            raise ValueError(f'Player with id {owner_id} not found')
        if player.game is not None:
            raise ValueError(f'Player with id {owner_id} is already in a game')
        if player.is_owner:
            raise ValueError(f'Player with id {owner_id} is already a game owner')
        
        game = Game(name=name, max_players=max_players)
        game.players.add(player)
        player.is_owner = True
        return game
    
    @db_session
    def get_game(self, id, include_players):
        game = Game.get(id=id)
        if game is None:
            raise ValueError(f'Game with id {id} not found')
        if include_players:
            dic = game.to_dict(related_objects=True, with_collections=True)
            dic['players'] = [p.to_dict() for p in dic['players']]
            return dic
        return game.to_dict()
    
    @db_session
    def get_game_players(self, game_id):
        game = Game.get(id=game_id)
        if game is None:
            raise ValueError(f'Game with id {game_id} not found')
        players = game.players
        return [p.to_dict() for p in players]
    

    @db_session
    def get_games(self, lobby=False):
        if lobby:
            lobbies = Game.select(lambda g: g.in_lobby)
            ret = []
            for l in lobbies:
                ret.append(l.to_dict())
                ret[-1]['active_players'] = len(l.players)
            
            return ret

        else:
            games = Game.select(lambda g: not g.in_lobby)
            return [g.to_dict() for g in games]
    
    @db_session
    def add_player_to_game(self, game_id, player_id):
        game = Game.get(id=game_id)
        if game is None:
            raise ValueError(f'Game with id {game_id} not found')
        if game.max_players == len(game.players):
            raise ValueError(f'Game with id {game_id} is full')
        
        player = Player.get(id=player_id)
        if player is None:
            raise ValueError(f'Player with id {player_id} not found')
        
        if player.game is not None:
            raise ValueError(f'Player with id {player_id} is already in a game')
        
        if game.in_lobby:
            game.players.add(player)
            return game
        else:
            raise ValueError(f'Game with id {game_id} is not in lobby')
        
    @db_session
    def remove_player_from_game(self, game_id, player_id):
        game = Game.get(id=game_id)
        if game is None:
            raise ValueError(f'Game with id {game_id} not found')
    
        player = Player.get(id=player_id)
        if player is None:
            raise ValueError(f'Player with id {player_id} not found')
        if player.game is None:
            raise ValueError(f'Player with id {player_id} is not in a game')
        if player.game.id != game.id:
            raise ValueError(f'Player with id {player_id} is not in game with id {game_id}')
        
        game.players.remove(player)
       
        if player.is_owner:
            player.is_owner = False
            if len(game.players) > 0:
                new_owner = list(game.players)[0]
                new_owner.is_owner = True
            else:
                game.delete()        

    @db_session
    def start_game(self, game_id, owner_id):
        game = Game.get(id=game_id)
        players: set = game.players

        if game is None:
            raise ValueError(f'Game with id {game_id} not found')
        if players.__len__() < 2:
            raise ValueError(f'Not enough players in game with id {game_id}')
        
        owner = Player.get(id=owner_id)
        if owner is None:
            raise ValueError(f'Player with id {owner_id} not found')
        if not owner.is_owner or owner.game.id != game.id:
            raise ValueError(f'Player with id {owner_id} is not the owner of game with id {game_id}')
        
        game.in_lobby = False
        return game
    
    @db_session
    def leave_game(self, game_id, player_id):
        game = Game.get(id=game_id)
        if game is None:
            raise ValueError(f'Game with id {game_id} not found')
        player = Player.get(id=player_id)
        if player is None:
            raise ValueError(f'Player with id {player_id} not found')
        if player.game is None:
            raise ValueError(f'Player with id {player_id} is not in a game')
        if player.game.id != game.id:
            raise ValueError(f'Player with id {player_id} is not in game with id {game_id}')
        
        player.game = None
        
        player.is_owner = False
        if len(game.players) == 0:
            game.delete()
        elif player.is_owner:
            new_owner = game.players.first()
            new_owner.is_owner = True

        return {'state': 'success',
                'message': f'Player with id {player_id} has left game with id {game_id}'}
    
    @db_session
    def game_over(self, game_id):
        game = Game.get(id=game_id)
        if game is None:
            raise ValueError(f'Game with id {game_id} not found')
        game.in_lobby = True
        print(game)
        

gs = GameService()
