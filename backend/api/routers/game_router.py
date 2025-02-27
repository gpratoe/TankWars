from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, HTTPException
from pydantic import BaseModel
from api.ws import manager
from db.game_handler import GameHandler

gr = APIRouter()
gh = GameHandler()

class GameSchema(BaseModel):
    name: str
    max_players: int
    owner_id: int

@gr.post(path="", status_code=status.HTTP_201_CREATED)
async def create_game(game_data: GameSchema):
    try:
        game = gh.create_game(game_data.name, game_data.max_players, game_data.owner_id)
        return game.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get_game(id:int):
    try:
        game = gh.get_game(id)
        return game.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.get(path="/{id}/players", status_code=status.HTTP_200_OK)
async def get_game_players(id:int):
    try:
        players = gh.get_game_players(id)
        return players
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.get(path="", status_code=status.HTTP_200_OK)
async def get_games(lobby:bool=False):
    try:
        if lobby:
            lobbies = gh.get_games(lobby=True)
            return lobbies
        else:
            games = gh.get_games()
            return games
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  
        
@gr.post(path="/{game_id}/players", status_code=status.HTTP_202_ACCEPTED)
async def add_player_to_game(game_id:int, player_id:int):
    try:
        game = gh.add_player_to_game(game_id, player_id)
        return game.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.delete("/{game_id}/players/{player_id}",status_code=status.HTTP_202_ACCEPTED)
async def remove_player_from_game(game_id:int, player_id:int):
    try:
        game = gh.remove_player_from_game(game_id, player_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@gr.post("/{game_id}/start", status_code=status.HTTP_202_ACCEPTED)
async def start_game(game_id:int, owner_id:int):
    try:
        game = gh.start_game(game_id, owner_id)
        return game.to_dict()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@gr.websocket("/testws")
async def websocket_endpoint(websocket: WebSocket, name: str):
    
    await manager.connect(websocket, name)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.handle_data(data)
            #game.run()
            # await manager.broadcast(json.dumps({
            #             "event": "state",
            #             "data": game.get_state()
            #         }), name)
            
            
    except WebSocketDisconnect:
        await manager.disconnect(name)
        print("dcd")