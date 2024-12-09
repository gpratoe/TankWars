from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from api.ws import manager
import json

gr = APIRouter()

@gr.websocket("/testws")
async def websocket_endpoint(websocket: WebSocket):
    
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        print("dcd")