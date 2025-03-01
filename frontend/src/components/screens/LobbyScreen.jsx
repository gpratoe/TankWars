import React, {useState, useEffect} from "react";
import { useParams } from 'react-router-dom';
import { get_game_players } from "../../apiService";
import Chat from "../Chat";
import "../../styles/LobbyScreen.css";


function LobbyScreen({}){
    const [players, setPlayers] = useState([]);
    const lobbyId = useParams().lobbyId;

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
                                    <button className='red-button' id='kick-button'>Expulsar</button>
                                </li>
                            </div>
                        )}
                    </ul>
                </div>
                <Chat/>
            </div>
            <button className='red-button'>Abandonar</button>
        </div>
    );
}

export default LobbyScreen;