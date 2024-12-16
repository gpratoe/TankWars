from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.tank import Tank
from typing import Tuple

tank = None

class Tank_schema(BaseModel):
    name: str
    pos: Tuple[int, int]
    direction: Tuple[float, float]
    damage: int
    bullet_speed: int

tr = APIRouter()

@tr.post("/new", status_code=status.HTTP_201_CREATED)
async def create_tank(tank: Tank_schema):
    tank = Tank(tank.name, tank.pos, tank.direction, tank.damage, tank.bullet_speed)
    print(tank.name, tank.pos, tank.direction, tank.damage, tank.bullet_speed)

@tr.post("/move", status_code=status.HTTP_200_OK)
async def move_tank(name: str, pos: Tuple[int, int], direction: Tuple[float, float]):
    tank.update_pos(pos, direction)