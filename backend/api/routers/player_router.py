from fastapi import APIRouter, status, HTTPException
from db.player_service import ps

pr = APIRouter()

@pr.post(path="", status_code=status.HTTP_201_CREATED)
async def create_player(name: str):
    player_id = ps.create_player(name)
    return {"id": player_id}

@pr.get(path="/{id}")
async def get_player(id: int):
    try:
        player = ps.get_player(id)
        return player
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code= status.HTTP_404_NOT_FOUND)