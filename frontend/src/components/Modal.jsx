import React from 'react'
import '../styles/Modal.css'

function Modal({ title, children, onClose }) {

  return (
    <div className='modal-overlay' onClick={onClose ? onClose : undefined}>
      <div className='modal-container' onClick={(e) => e.stopPropagation()}>
        <h1>{title}</h1>
        <div className='modal-children'>{children}</div>
      </div>
    </div>
  );
}

export default Modal;
