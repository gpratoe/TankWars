import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Game } from '../../game'; // Importa la instancia game
import { usePlayer } from '../contexts/playerContext';
import { useWebSocket } from '../contexts/webSocketContext';
import '../../styles/GameScreen.css';
import { WS_URL, leave_lobby } from '../../apiService';
import GameOverModal from '../GameOverModal.jsx'

function GameScreen({ }) {
  const { player, updatePlayer } = usePlayer();
  const lobbyId = useParams().lobbyId;
  const settings = JSON.parse(sessionStorage.getItem('game_settings'));
  const gameRef = useRef(null);
  const ws_url = `${WS_URL}/game/${lobbyId}/ws?player_id=${player.id}`;
  const navigate = useNavigate();
  const [winner, setWinner] = useState(null);

  const onMessage = useCallback((data) => {
    if (gameRef.current){
      gameRef.current.handleWebSocketMessage(data);
    }
  }, []);
  const {ws, sendMessage} = useWebSocket(ws_url, onMessage);

  const onGameOver = (winner) => { setWinner(winner) };

  useEffect(() => {
    const gameContainer = document.getElementById('game-container');

    const asyncInit = async () => {
      if(!gameRef.current){
        gameRef.current = new Game(settings, lobbyId, player.id, (data) => {sendMessage(data)}, onGameOver);
        await gameRef.current.init();
      
        if (ws.readyState === WebSocket.OPEN){
          sendMessage({event: 'player_ready', payload: {player_id: player.id}});
        }
        else{
          await new Promise((resolve) => {
            ws.onopen = () => {
              sendMessage({event: 'player_ready', payload: {player_id: player.id}});
              resolve();
            }
          });
        }
      }

    };

    asyncInit();

  }, [lobbyId, player.id, settings, sendMessage]);

  const onLeaving = async () => {
      try {
          const resp = await leave_lobby(lobbyId, player.id);
          updatePlayer({ id: player.id, name: player.name, is_owner: false });
          navigate('/rooms');
      }   
      catch(err) {
          console.error(err);
      }
  }
 
  return (
      <div className='gameScreen-container'>
        { winner && <GameOverModal winner={winner} onLeave={ async () => {await onLeaving()} } onGoBack={() => navigate(`/lobby/${lobbyId}`)}/> }
        <h1>Game</h1>
        <div id='game-container'></div>
      </div>
  );
}

export default GameScreen;
