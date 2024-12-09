from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.tanks_router import tr
from api.routers.game_router import gr, websocket_endpoint

app = FastAPI()

# Configurar CORS para permitir todas las solicitudes (en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gr, prefix="/game", tags=["game"])
app.include_router(tr, prefix="/tanks", tags=["tanks"])
app.add_websocket_route("/game/testws", websocket_endpoint)