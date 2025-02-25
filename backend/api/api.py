from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.player_router import pr
from api.routers.game_router import gr, websocket_endpoint
import asyncio
from src.game import game

async def start_game():
    asyncio.create_task(game.run())

app = FastAPI(on_startup=[start_game])

# Configurar CORS para permitir todas las solicitudes (en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gr, prefix="/game", tags=["game"])
app.include_router(pr, prefix="/player", tags=["player"])
app.add_websocket_route("/game/testws", websocket_endpoint)