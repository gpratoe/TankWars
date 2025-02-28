import React, {useState, useEffect} from "react";
import { useParams } from 'react-router-dom';
import { get_game_players } from "../../apiService";

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
            <h1>Lobby</h1>
            <div className="lobbyPlayers">
                <h2>Jugadores</h2>
                <ul>
                    {players.map((player, i) =>
                        <li key={i}>
                            <p style={{'color':`${player.color}`}}>{player.name}</p>
                        </li>
                    )}
                </ul>
            </div>
        </div>
    );
}

export default LobbyScreen;