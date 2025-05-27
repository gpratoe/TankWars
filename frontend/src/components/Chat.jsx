import React, {useState, useCallback, useRef, useEffect} from "react";
import '../styles/Chat.css';
import Button from "./Button";
import { useWebSocket } from "./contexts/webSocketContext";
import { usePlayer } from "./contexts/playerContext";
import { useParams } from 'react-router-dom';
import { WS_URL } from "../apiService";

function Chat ({}) {
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState('');
    const { player, updatePlayer } = usePlayer();
    const lobbyId = useParams().lobbyId;
    const ws_url = `${WS_URL}/game/${lobbyId}/ws?player_id=${player.id}`;

    const onMessage = useCallback((data) => {
        if (data.event === 'chat_msg') {
            const payload = data.payload;
            const msg = payload.msg;
            const sender = payload.sender;
            const time = payload.time;
            const newMessage = {sender: sender, text: msg};
            setMessages((prevMessages) => {
                return [...prevMessages, newMessage];
            });
        }
    }, []);


    const {ws, sendMessage} = useWebSocket(ws_url, onMessage);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (message.trim()){
            sendMessage({
                event: 'chat_msg',
                payload: {
                    msg: message,
                    sender: player.name,
                }
            });
            setMessage('');
        }
    }

    return (
        <div className="chat-container">
            <h2>Chat</h2>
            <ol id="chat-list">
                {messages.map((m, i) =>
                    <li key={i}>
                        <div className='chat-entry'>
                        <p id='sender'>{m.sender}:</p>
                        <p id='message'> {m.text}</p>
                        </div>
                    </li>
                )}
            </ol>
            <form id="chat-sendbar" onSubmit={handleSubmit}>
                <input type="text" id="chat-input"
                     autoComplete="off"
                     placeholder="Escribe un mensaje"
                     value={message}
                     onChange={(e) => {
                            setMessage(e.target.value);
                     }}></input>
                <Button text='Enviar' id="chat-send" btn_type='submit'/>
            </form>
        </div>
    );
}

export default Chat;
