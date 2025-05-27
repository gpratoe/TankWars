import React, {useState, useEffect, useCallback} from "react";
import { useParams, useNavigate } from 'react-router-dom';
import { get_game_players, leave_lobby, start_game, WS_URL } from "../../apiService";
import Chat from "../Chat";
import "../../styles/LobbyScreen.css";
import Button from "../Button";
import { useWebSocket, WebSocketContext } from "../contexts/webSocketContext";
import { usePlayer } from "../contexts/playerContext";


function LobbyScreen({}){
    const [players, setPlayers] = useState([]);
    const { player, updatePlayer } = usePlayer();
    const lobbyId = useParams().lobbyId;
    const navigate = useNavigate();

    const ws_url = `${WS_URL}/game/${lobbyId}/ws?player_id=${player.id}`;
    
    const onMessage = useCallback((data) => {
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
            if (data.owner && data.owner === player.id){
                updatePlayer({ id: player.id, name: player.name, is_owner: true });
            }
        }
        else if (data.event === 'game_started'){
            navigate(`/game/${lobbyId}`);
        }
        else if (data.event === 'game_settings'){
            sessionStorage.setItem('game_settings', JSON.stringify(data.payload));
        }
    }, []);
    
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
            const resp = await leave_lobby(lobbyId, player.id);
            updatePlayer({ id: player.id, name: player.name, is_owner: false }); // this re-renders the lobby and calls for useWebSocket generating a rejected conection due to player not in game anymore (not problematic but annoying)
            navigate('/rooms');
        }   
        catch(err) {
            console.error(err);
        }
    }
    
    const onStart = async () => {
        try{
            const resp = await start_game(lobbyId, player.id);
            navigate(`/game/${lobbyId}`);
        }
        catch(err){
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
                        {players.map((p, i) =>
                            <div className='list-item' key={i} id={p.color}>
                                <div className='color-show'></div>
                                <li>
                                    <p>{p.name}</p>
                                    {player.is_owner && <Button text='Expulsar' variant='red' id='kick-button'/>}
                                </li>
                            </div>
                        )}
                    </ul>
                </div>
                <div className='chat-wrapper'>
                    <Chat/>
                </div>
           </div>
            <div className='buttons-container'>
                <Button text='Abandonar' variant='red' onClick={() => {onLeaving()}}/>
                {player.is_owner ? <Button text='Empezar' onClick={() => {onStart()}}/>: null}
            </div>
        </div>
    );
}

export default LobbyScreen;
