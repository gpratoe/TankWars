from fastapi.websockets import WebSocket, WebSocketState
import asyncio
from src.utils import utils

class ConnectionManager:
    def __init__(self, id):
        self.id = id
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, connection: WebSocket, player_id: int):
        try:    
            await connection.accept()
            self.active_connections[player_id] = connection
        
        except Exception as e:
            utils.logger.warning(e, " conection failed")
            if player_id in self.active_connections:
                self.active_connections.pop(player_id)

    async def disconnect(self, player_id: int):
        try:
           if player_id in self.active_connections:
                if self.active_connections[player_id].client_state == WebSocketState.CONNECTED:
                    await self.active_connections[player_id].close()
                self.active_connections.pop(player_id)

        except Exception as e:
            utils.logger.warning(f"Error during disconnection of player with id: {player_id}: {e}")

    async def broadcast(self, data: dict):
        to_remove = []
        for player_id, connection in self.active_connections.items():
            try:
                await connection.send_json(data)
            except Exception as e:
                utils.logger.warning(f"Error broadcasting to player {player_id}: {e}")
                to_remove.append(player_id)

        for player_id in to_remove:
            await self.disconnect(player_id)

    async def send_message(self, data: dict, player_id: int):
        try:
            if player_id in self.active_connections:
                await self.active_connections[player_id].send_json(data)
        except Exception as e:
            utils.logger.warning(f"Error sending message to player with id: {player_id} in lobby: {self.id}: {e}")



#manager = ConnectionManager()