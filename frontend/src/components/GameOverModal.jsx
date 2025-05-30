import React from 'react';
import Modal from './Modal.jsx'
import Button from './Button.jsx'
import '../styles/GameOverModal.css'

function GameOverModal({ winner, onLeave, onGoBack }) {
  return (
    <Modal title={`¡${winner} Ganó!`}>
      <div className='gomodal-container'>
        <p>Volviendo al lobby en 3..</p>
        <div className='button-container'>
          <Button text='Abandonar' variant='red' onClick={ onLeave }/>
          <Button text='Volver al lobby' onClick={ onGoBack }/>
        </div>
        </div>
    </Modal>
  );
}

export default GameOverModal;
