import { createContext, useEffect, useRef, useContext } from "react";
import { on } from "ws";

export const WebSocketContext = createContext(undefined);

export function WebSocketProvider({ children }) {
    const webSockets = useRef({});
    const callBacks = useRef({});

    const subscribe = (url, callBack) => {
        if (!callBacks.current[url]) {
            callBacks.current[url] = [];
        }
        callBacks.current[url].push(callBack);
    }

    const createWebSocket = (url) => {
        const ws = new WebSocket(url);
        ws.onopen = () => {
            console.log(`Connected to ${url}`);
            ws.send(JSON.stringify({ event: 'connect' }));
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (callBacks.current[url]) {
                callBacks.current[url].forEach((cb) => {
                    cb(data);
                });
            }
        };
        ws.onclose = () => {
            console.log(`Disconnected from ${url}`);
            delete webSockets.current[url];
            delete callBacks.current[url];
        }

        return ws;
    };
    
    const sendMessage = (url, message) => {
        const ws = getWebSocket(url); 
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(message)); 
        } else {
            console.warn(`WebSocket for ${url} is not open. Current state: ${ws.readyState}`);
        }
    };

    const getWebSocket = (url) => {
        if (!webSockets.current[url]) {
            webSockets.current[url] = createWebSocket(url);
            callBacks.current[url] = [];
        }
        return webSockets.current[url];
    };

    // cleanup
    useEffect(() => {
        return () => {
            Object.values(webSockets.current).forEach(ws => ws.close());
            webSockets.current = {};
            callBacks.current = {};
        };
    }, []);

    return (
        <WebSocketContext.Provider value ={{ getWebSocket, subscribe, sendMessage }}>
            {children}
        </WebSocketContext.Provider>
    );
}

// custom hook to get the websocket
export function useWebSocket(url, onMessage) {
    const context = useContext(WebSocketContext);
    
    if (!context) {
        throw new Error('Not in provider wachin');
    }
    
    const { getWebSocket, subscribe, sendMessage} = context;
    const ws = getWebSocket(url);

    useEffect(()=>{
        if (onMessage) {
            subscribe(url, onMessage);
        }
    }, [url, onMessage, subscribe]);
    
    return {ws, sendMessage: (message) => sendMessage(url, message)};
}