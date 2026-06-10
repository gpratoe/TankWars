from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, HTTPException
from pydantic import BaseModel
from db.game_service import gs
from src.lobby import Lobby
from src.player import Player
from src.game_state_machine import GameStateMachine
from src.utils import utils

gr = APIRouter()

class GameSchema(BaseModel):
    name: str
    max_players: int
    owner_id: int

@gr.post(path="", status_code=status.HTTP_201_CREATED)
async def create_game(game_data: GameSchema):
    try:
        owner = Player("", game_data.owner_id)
        lobby, resp = Lobby.new(game_data.name, owner, game_data.max_players)
        gsm = GameStateMachine.new(lobby)
        return resp
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get_game(id:int, include_players:bool=False):
    try:
        game = gs.get_game(id, include_players)
        return game
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.get(path="/{id}/players", status_code=status.HTTP_200_OK)
async def get_game_players(id:int):
    try:
        lobby = GameStateMachine.get_gsm(id).lobby
        players = lobby.get_players()
        return players
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.get(path="", status_code=status.HTTP_200_OK)
async def get_games(lobby:bool=False):
    try:
        if lobby:
            lobbies = gs.get_games(lobby=True)
            return lobbies
        else:
            games = gs.get_games()
            return games
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  
        
@gr.post(path="/{game_id}/players", status_code=status.HTTP_202_ACCEPTED)
async def add_player_to_game(game_id:int, player_id:int):
    try:
        lobby = GameStateMachine.get_gsm(game_id).lobby
        player = Player("", player_id)
        color = lobby.add_player(player)
        return {'message': 'Player added to game',
                'color': color}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.delete("/{game_id}/players/{player_id}",status_code=status.HTTP_202_ACCEPTED)
async def remove_player_from_game(game_id:int, player_id:int):
    try:
        gsm = GameStateMachine.get_gsm(game_id)
        await gsm.handle_disconnect(player_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@gr.post("/{game_id}/kick/{player_to_kick_id}", status_code=status.HTTP_202_ACCEPTED)
async def kick_player(game_id:int, owner_id:int, player_to_kick_id:int):
    try:
        gsm = GameStateMachine.get_gsm(game_id)
        lobby = gsm.lobby
        resp = await lobby.kick_player(owner_id, player_to_kick_id)
        return resp
    except Exception as e:
        utils.logger.warning(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.post("/{game_id}/start", status_code=status.HTTP_202_ACCEPTED)
async def start_game(game_id:int, owner_id:int):
    try:
        gsm = GameStateMachine.get_gsm(game_id)
        resp = await gsm.start_game(owner_id)
        return resp
    except Exception as e:
        utils.logger.warning(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@gr.websocket("/{game_id}/ws")
async def game_lobby_ws(websocket: WebSocket, game_id: int, player_id: int):
    try:
        gsm = GameStateMachine.get_gsm(game_id)
        lobby = gsm.lobby
        await lobby.connect_player(player_id, websocket)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    while True:
        try:
            data = await websocket.receive_json()
            if data:
                await gsm.handle_data(data, player_id)

        except WebSocketDisconnect:
            try:
                await gsm.handle_disconnect(player_id)
            except Exception as e:
                utils.logger.warning(str(e))
            break
