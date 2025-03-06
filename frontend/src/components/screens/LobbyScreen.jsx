import React, {useState, useEffect} from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { get_game_players, leave_lobby } from "../../apiService";
import Chat from "../Chat";
import "../../styles/LobbyScreen.css";
import Button from "../Button";
import { useWebSocket, WebSocketContext } from "../contexts/webSocketContext";


function LobbyScreen({}){
    const [players, setPlayers] = useState([]);
    const lobbyId = useParams().lobbyId;
    const navigate = useNavigate();
    const ws_url = `ws://localhost:8000/game/${lobbyId}/ws?player_id=${sessionStorage.getItem('playerId')}`;
    
    const onMessage = (data) => {
        console.log(data.player);
        if (data.event === 'player_joined') {
            const newPlayer = data.player;
            if (newPlayer){
                setPlayers((prevPlayers) => {
                    if (prevPlayers.find(player => player.id === newPlayer.id)){
                        return prevPlayers;
                    } else {
                        return [...prevPlayers, newPlayer];
                    }
                })
            }
        }
        else if (data.event === 'player_left'){
            const playerId = data.player_id;
            setPlayers((prevPlayers) => {
                return prevPlayers.filter(player => player.id !== playerId);
            });
        } 
    }
    
    const ws = useWebSocket(ws_url, onMessage);
    
    useEffect(() => {
        async function fetchPlayers(){
            try{
                
                const data = await get_game_players(lobbyId);
                setPlayers(data);
            }
            catch(err){
                console.error(err);
            }
        }
        fetchPlayers();
    }, []);

    const onLeaving = async () => {
        try {
            const resp = await leave_lobby(lobbyId, sessionStorage.getItem('playerId'));
            ws.close();
            navigate('/lobby');
        }   
        catch(err) {
            console.error(err);
        }
    }
    
    return (
        <div className="lobbyScreen">
            <h1>LOBBY</h1>
            <div className="lobbyInfo">
                <div className="lobbyPlayers">
                    <h2>JUGADORES</h2>
                    <ul>
                        {players.map((player, i) =>
                            <div className='list-item' key={i} id={player.color}>
                                <div className='color-show'></div>
                                <li>
                                    <p>{player.name}</p>
                                    <Button text='Expulsar' variant='red' id='kick-button'/>
                                </li>
                            </div>
                        )}
                    </ul>
                </div>
                <Chat/>
            </div>
            <Button text='Abandonar' variant='red' onClick={() => {onLeaving()}}/>
        </div>
    );
}

export default LobbyScreen;