from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.tanks_router import tr
app = FastAPI()

# Configurar CORS para permitir todas las solicitudes (en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tr, prefix="/tanks", tags=["tanks"])