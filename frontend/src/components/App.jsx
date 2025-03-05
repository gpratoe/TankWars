import React, { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import NameScreen from './screens/NameScreen';
import JoinCreateScreen from './screens/JoinCreateScreen';
import GameScreen from './screens/GameScreen';
import LobbyScreen from './screens/LobbyScreen';
import '../styles/App.css';
import { WebSocketProvider } from '../webSocketContext';

function App() {

  return (
    <div style={{ fontFamily: 'Arial', textAlign: 'center' }}>
      <WebSocketProvider>
        <Routes>
          <Route
            path="/"
            element={<NameScreen />}
          />
          <Route
            path="/lobby"
            element={
              <JoinCreateScreen/>
            }
          />
          <Route
            path="/lobby/:lobbyId"
            element={<LobbyScreen />}
          />
          <Route
            path="/game/:lobbyId"
            element={<GameScreen />}
          />
          
        </Routes>
      </WebSocketProvider>
    </div>
  );
}

export default App;