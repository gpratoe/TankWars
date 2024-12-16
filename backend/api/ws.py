from fastapi.websockets import WebSocket
from src.game import game
import json
from src.utils import utils
import asyncio

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
            if name in self.active_connections:
                self.active_connections.pop(name, None)

    async def disconnect(self, name: str):
        try:
            if name in self.active_connections:
                self.active_connections.pop(name)
            if name in game.tanks:
                game.tanks[name].tank.DestroyFixture(game.tanks[name].tank.fixtures[0])
                game.tanks.pop(name)

            await self.broadcast(json.dumps({
                "event": "remove_tank",
                "data": name
            }), name)
        except Exception as e:
            print(f"Error during disconnection of {name}: {e}")

    async def broadcast(self, data: str, name: str = None):
        for conn_name, connection in self.active_connections.items():
            #if name is None or conn_name != name:  # Solo excluye si `name` es válido.
            try:
                await connection.send_text(data)
            except Exception as e:
                print(f"Error broadcasting to {conn_name}: {e}")


    async def handle_data(self, data: str):
        try:
            parsed = json.loads(data)
            event = parsed.get("event")
            data = parsed.get("data")

            if event == "state" and "name" in data:
                name = data["name"]
                if name in game.tanks:
                    tank = game.tanks[name]
                    tank.set_state(data)
            
        except json.JSONDecodeError as e:
            print(f"Invalid JSON received: {data} - {e}")
        except KeyError as e:
            print(f"Missing key in data: {data} - {e}")
        except Exception as e:
            print(f"Unexpected error handling data: {data} - {e}")



manager = utils.manager = connection_manager()