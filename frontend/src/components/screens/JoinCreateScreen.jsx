import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import { get_lobbies, join_game } from '../../apiService';
import '../../styles/JoinCreateScreen.css';
import CreateGameForm from '../CreateGameForm';

function JoinCreateScreen({}) {
  const [lobbies, setLobbies] = useState([]);
  const [createGame, setCreateGame] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    async function fetch_lobbies(){
      try{
        const data = await get_lobbies();
        setLobbies(data);
        console.log(data);
      }
      catch(err){
        console.error(err);
      }
    }

    fetch_lobbies();
  }, []);

  const handleJoinGame = async (lobby_id) => {
    const playerId = sessionStorage.getItem('playerId');
    if (playerId){
      try {
        await join_game(lobby_id, playerId);
        navigate(`/lobby/${lobby_id}`);
      }
      catch(err){
        console.error(err);
      }
    }
  }

  return (
    <div className="join-create-screen">
      
      { createGame ? (
        <div>
          <CreateGameForm goBackFunc={setCreateGame}/>
        </div>
      ):(
        <>
          <h1>SALAS</h1>
          <button className='green-button' id='boton-crear' onClick = {() => setCreateGame(true)}>Crear sala</button>
          <ul>
            {lobbies.map((lobby, i) =>
            <li key={i}>
              <p>{lobby.name} (#{lobby.id}) - Jugadores: <span style={{color: 'red'}}>{lobby.active_players}</span>/{lobby.max_players}</p>
              <button className='green-button' onClick={() => {handleJoinGame(lobby.id)}}>Unirse</button>
            </li>  
            )}
          </ul>
        </>
      )}
    </div>
  );
}

export default JoinCreateScreen;