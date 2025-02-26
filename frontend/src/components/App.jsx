import React, { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import NameScreen from './screens/NameScreen';
import LobbyScreen from './screens/LobbyScreen';
import GameScreen from './screens/GameScreen';

function App() {

  return (
    <div style={{ fontFamily: 'Arial', textAlign: 'center' }}>
      <Routes>
        <Route
          path="/"
          element={<NameScreen />}
        />
        <Route
          path="/lobbies"
          element={
            <LobbyScreen
              
            />
          }
        />
        <Route
          path="/game/:lobbyId"
          element={<GameScreen />}
        />
      </Routes>
    </div>
  );
}

export default App;