export class WebSocketManager {
    constructor(url, name, onMessageCallback) {
        this.name = name;
        this.url = url;
        this.ws = new WebSocket(`${url}?name=${name}`);
        this.ws.onmessage = (event) => {
            const fullData = JSON.parse(event.data);
            if (onMessageCallback) {
                onMessageCallback(fullData);
            }
        };
    }

    send(event, data) {
        if (this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ event, data }));
        }
    }

    close() {
        this.ws.close();
    }
}
