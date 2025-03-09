import React, { useCallback, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Game } from '../../game'; // Importa la instancia game
import { usePlayer } from '../contexts/playerContext';
import { useWebSocket } from '../contexts/webSocketContext';
import '../../styles/GameScreen.css';
import { WS_URL } from '../../apiService';

function GameScreen({ }) {
  const { player } = usePlayer();
  const lobbyId = useParams().lobbyId;
  const settings = JSON.parse(sessionStorage.getItem('game_settings'));
  const gameRef = useRef(null);
  const ws_url = `${WS_URL}/game/${lobbyId}/ws?player_id=${player.id}`;

  const {ws, sendMessage} = useWebSocket(ws_url, (data) => {
    if (gameRef.current){
      gameRef.current.handleWebSocketMessage(data);
    }
  });


  useEffect(() => {
    const gameContainer = document.getElementById('game-container');

    const asyncInit = async () => {
      if(!gameRef.current){
        gameRef.current = new Game(settings, lobbyId, player.id, (data) => {sendMessage(data)});
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

  return (
    <div className='gameScreen-container'>
      <h1>Game</h1>
      <div id='game-container'></div>
    </div>
  );
}

export default GameScreen;