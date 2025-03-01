import React, {useState, useEffect} from "react";
import '../styles/Chat.css';

function Chat ({}) {
    const [messages, setMessages] = useState([]);
    
    useEffect(() => {
        setMessages([
            {sender: 'Jugador1', text: 'Hola'},
            {sender: 'Jugador2', text: 'Hola'},
            {sender: 'Jugador1', text: 'Como estas?'},
            {sender: 'Jugador2', text: 'Bien, y tu?'},
            {sender: 'Jugador1', text: 'Tambien'},
            {sender: 'Jugador2', text: 'Que bien'},
            {sender: 'Jugador1', text: 'Si'},
            {sender: 'Jugador2', text: '...'},
        ]);
    }, []);
    return (
        <div className="chat-container">
            <h2>Chat</h2>
            <ol id="chat-list">
                {messages.map((message, i) =>
                    <li key={i}>
                        <div className='chat-entry'>
                        <p>{message.sender}:</p>
                        <p> {message.text}</p>
                        </div>
                    </li>
                )}
            </ol>
            <div id="chat-sendbar">
                <input type="text" id="chat-input" placeholder="Escribe un mensaje"></input>
                <button className='green-button' id="chat-send">Enviar</button>
            </div>
        </div>
    );
}

export default Chat;