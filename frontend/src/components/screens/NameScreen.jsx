import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { create_player } from '../../apiService';
import Button from '../Button';
import '../../styles/NameScreen.css';

function NameScreen() {
  const [inputName, setInputName] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError(null);
    setLoading(true)

    if (inputName.trim()) {
      try{
        const data = await create_player(inputName);
        if (data && data.id) {
          sessionStorage.setItem('playerId', data.id);
          navigate('/lobby');
        }
        else{
          setLoading(false);
          throw new Error('No se pudo obtener el id del jugador');
        }
      }
      catch(err){
        setLoading(false);
        setError(err.message);
      }
    }
  };

  return (
    <div className='nameScreen'>
      <h1>Elige tu nombre</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputName}
          onChange={(e) => setInputName(e.target.value)}
          placeholder="Ingresa tu nombre"
          maxLength={16}
        />
        <Button
          text='Continuar'
          btn_type="submit"
          disabled={loading}
        />
      </form>
      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
}

export default NameScreen;