import React, { useCallback, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Game } from '../../game'; // Importa la instancia game
import { usePlayer } from '../contexts/playerContext';

function GameScreen({ }) {
  const player = usePlayer();
  const lobbyId = useParams().lobbyId;
  const settings = JSON.parse(sessionStorage.getItem('game_settings'));
  const  game = useRef(new Game(settings,lobbyId, player.id));

  useEffect(() => {
    const gameContainer = document.getElementById('game-container');
    
    const initGame = async () => {
      await game.current.init();
      game.current.update();
    };

    initGame().catch(console.error);

  }, []);

  return (
    <div>
      <h1>Game</h1>
      <div id='game-container'></div>
    </div>
  );
}

export default GameScreen;