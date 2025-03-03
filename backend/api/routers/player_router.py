from fastapi import APIRouter, status, HTTPException
from db.player_service import PlayerService

pr = APIRouter()
ps = PlayerService()

@pr.post(path="", status_code=status.HTTP_201_CREATED)
async def create_player(name: str):
    player_id = ps.create_player(name)
    return {"id": player_id}

@pr.get(path="/{id}")
async def get_player(id: int):
    try:
        player = ps.get_player(id)
        return player.to_dict()
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code= status.HTTP_404_NOT_FOUND)