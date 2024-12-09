from fastapi.websockets import WebSocket

class connection_manager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, connection: WebSocket):
        try:
            await connection.accept()
            self.active_connections.append(connection)
        except Exception as e:
            print(e, " conection failed")
    
    async def disconnect(self, connection: WebSocket):
        self.active_connections.remove(connection)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)



manager = connection_manager()