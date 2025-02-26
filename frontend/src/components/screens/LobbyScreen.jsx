import React from 'react';
import { useNavigate } from 'react-router-dom';

function LobbyScreen({}) {
  const navigate = useNavigate();

  return (
    <div>
      <h1>Lobbies</h1>
    </div>
  );
}

export default LobbyScreen;