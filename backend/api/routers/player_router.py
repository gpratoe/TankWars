from fastapi import APIRouter, status, HTTPException
from db.player_handler import PlayerHandler

pr = APIRouter()
ph = PlayerHandler()

@pr.post(path="/", status_code=status.HTTP_201_CREATED)
async def create_player(name: str):
    player = ph.create_player(name)
    return {"id": player.id}

@pr.get(path="/{id}")
async def get_player(id: int):
    try:
        player = ph.get_player(id)
        return player.to_dict()
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code= status.HTTP_404_NOT_FOUND)