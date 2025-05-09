from fastapi.websockets import WebSocket, WebSocketState


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, connection: WebSocket, lobby_id: int, player_id: int):
        try:    
            await connection.accept()
            self.active_connections[player_id] = connection
        
        except Exception as e:
            print(e, " conection failed")
            if player_id in self.active_connections:
                self.active_connections.pop(player_id)

    async def disconnect(self, lobby_id: int, player_id: int):
        try:
           if player_id in self.active_connections:
                if self.active_connections[player_id].client_state == WebSocketState.CONNECTED:
                    await self.active_connections[player_id].close()
                self.active_connections.pop(player_id)

        except Exception as e:
            print(f"Error during disconnection of player with id: {player_id}: {e}")

    async def broadcast(self, data: dict, lobby_id: int):
        connections_copy = self.active_connections.copy()
        for player_id, connection in connections_copy.items():
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"Error broadcasting to player with id: {player_id} in lobby: {lobby_id}: {e}")

    async def send_message(self, data: dict, lobby_id: int, player_id: int):
        try:
            if player_id in self.active_connections:
                await self.active_connections[player_id].send_json(data)
        except Exception as e:
            print(f"Error sending message to player with id: {player_id} in lobby: {lobby_id}: {e}")



#manager = ConnectionManager()