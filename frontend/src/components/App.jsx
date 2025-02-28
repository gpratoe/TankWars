import React, { useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import NameScreen from './screens/NameScreen';
import JoinCreateScreen from './screens/JoinCreateScreen';
import GameScreen from './screens/GameScreen';
import '../styles/App.css';

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
            <JoinCreateScreen/>
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