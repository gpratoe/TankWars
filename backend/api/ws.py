from fastapi.websockets import WebSocket
from src.game import game
import json

class connection_manager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, connection: WebSocket, name: str):
        try:
            await connection.accept()
            if game.add_tank(name):
                print("tank not added")
                await connection.send_text("tank already exists")
                return
            else:
                print("tank added")
                self.active_connections[name] = connection
                await connection.send_text(json.dumps({
                    "event": "init_tank",
                    "data":
                    game.tanks[name].get_state()}))
        
        except Exception as e:
            print(e, " conection failed")
    
    async def disconnect(self, name: str):
        self.active_connections.pop(name)
        game.tanks.pop(name)

    async def broadcast(self, data: str, name: str):
        for connection in self.active_connections.values():
            if connection != self.active_connections[name]:
                await connection.send_text(data)

    async def handle_data(self, data: str):
        print(data)
        event = json.loads(data)["event"]
        data = json.loads(data)["data"]

        if event == "add_tank":
            pass # maybe i dont need this
        elif event == "state":
            tank = game.tanks[data["name"]]
            tank.set_state(data)
            tank.update()
            await self.broadcast(json.dumps({
                "event": "state",
                "data":tank.get_state()
                }), data["name"])    
        
        game.run()



manager = connection_manager()