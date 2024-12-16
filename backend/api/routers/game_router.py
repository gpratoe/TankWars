from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.ws import manager


gr = APIRouter()

@gr.websocket("/testws")
async def websocket_endpoint(websocket: WebSocket, name: str):
    
    await manager.connect(websocket, name)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.handle_data(data)
            #game.run()
            # await manager.broadcast(json.dumps({
            #             "event": "state",
            #             "data": game.get_state()
            #         }), name)
            
            
    except WebSocketDisconnect:
        await manager.disconnect(name)
        print("dcd")