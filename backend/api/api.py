from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.player_router import pr
from api.routers.game_router import gr, game_lobby_ws
from src.light_numba_functions import warmup_numba_functions

warmup_numba_functions()
app = FastAPI()
# Configurar CORS para permitir todas las solicitudes (en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gr, prefix="/game", tags=["game"])
app.include_router(pr, prefix="/player", tags=["player"])
app.add_websocket_route("/game/{game_id}/ws", game_lobby_ws)
