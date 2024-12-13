from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from api.ws import manager

gr = APIRouter()

@gr.websocket("/testws")
async def websocket_endpoint(websocket: WebSocket, name: str):
    
    await manager.connect(websocket, name)
    try:
        while True:
            data = await websocket.receive_text()
            print("ep: \n", data)
            await manager.handle_data(data)
            
    except WebSocketDisconnect:
        await manager.disconnect(name)
        print("dcd")