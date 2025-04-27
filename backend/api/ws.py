from fastapi.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, connection: WebSocket, lobby_id: int, player_id: int):
        try:    
            await connection.accept()
            if lobby_id not in self.active_connections:
                self.active_connections[lobby_id] = {}
            self.active_connections[lobby_id][player_id] = connection
        
        except Exception as e:
            print(e, " conection failed")
            if lobby_id in self.active_connections and player_id in self.active_connections[lobby_id]:
                self.active_connections[lobby_id].pop(player_id)

    async def disconnect(self, lobby_id: int, player_id: int):
        try:
           if lobby_id in self.active_connections and player_id in self.active_connections[lobby_id]:
                if self.active_connections[lobby_id][player_id].client_state == 'connected':
                    await self.active_connections[lobby_id][player_id].close()
                self.active_connections[lobby_id].pop(player_id)

        except Exception as e:
            print(f"Error during disconnection of player with id: {player_id}: {e}")

    async def broadcast(self, data: dict, lobby_id: int):
        if lobby_id not in self.active_connections:
            return
        for player_id, connection in self.active_connections[lobby_id].items():
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"Error broadcasting to player with id: {player_id} in lobby: {lobby_id}: {e}")

    async def send_message(self, data: dict, lobby_id: int, player_id: int):
        try:
            if lobby_id in self.active_connections and player_id in self.active_connections[lobby_id]:
                await self.active_connections[lobby_id][player_id].send_json(data)
        except Exception as e:
            print(f"Error sending message to player with id: {player_id} in lobby: {lobby_id}: {e}")



manager = ConnectionManager()