import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import { get_lobbies, join_game } from '../../apiService';
import '../../styles/JoinCreateScreen.css';
import CreateGameForm from '../CreateGameForm';
import Button from '../Button';
import { usePlayer } from '../contexts/playerContext';

function JoinCreateScreen({}) {
  const [lobbies, setLobbies] = useState([]);
  const [createGame, setCreateGame] = useState(false);
  const [refresh, setRefresh] = useState(false);
  const { player, updatePlayer } = usePlayer();

  const navigate = useNavigate();

  useEffect(() => {
    async function fetch_lobbies(){
      try{
        const data = await get_lobbies();
        setLobbies(data);
      }
      catch(err){
        console.error(err);
      }
    }

    fetch_lobbies();
    setRefresh(false);
  }, [refresh]);

  const handleJoinGame = async (lobby_id) => {
    if (player.id){
      try {
        await join_game(lobby_id, player.id);
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
          <div className='buttons-container'>
            <Button text='Crear sala'onClick = {() => setCreateGame(true)}/>
            <Button text='Recargar salas'onClick = {() => setRefresh(true)}/>
          </div>
          <ul>
            {lobbies.map((lobby, i) =>
            <li key={i}>
              <p>{lobby.name} (#{lobby.id}) - Jugadores: <span style={{color: 'red'}}>{lobby.active_players}</span>/{lobby.max_players}</p>
              <Button text='Unirse' onClick={() => {handleJoinGame(lobby.id)}}/>
            </li>  
            )}
          </ul>
        </>
      )}
    </div>
  );
}

export default JoinCreateScreen;