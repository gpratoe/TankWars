import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function NameScreen() {
  const [inputName, setInputName] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputName.trim()) {
      navigate('/lobbies');
    }
  };

  return (
    <div>
      <h1>Elige tu nombre</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputName}
          onChange={(e) => setInputName(e.target.value)}
          placeholder="Ingresa tu nombre"
          style={{ padding: '8px', fontSize: '16px' }}
        />
        <button
          type="submit"
          style={{ marginLeft: '10px', padding: '8px 16px' }}
        >
          Continuar
        </button>
      </form>
    </div>
  );
}

export default NameScreen;