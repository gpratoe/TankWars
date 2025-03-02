import React from "react";
import '../styles/Button.css';

function Button({ text, type, onClick, variant='default', disabled=false }) {
    const color = variant === 'red' ? 'red' : 'green';

    return (
        <button type={type} onClick={onClick} className={`${color}-button`} disabled={disabled}>{text}</button>
    );
}

export default Button;