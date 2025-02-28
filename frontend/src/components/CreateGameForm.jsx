import React, { useState } from "react";
import { create_game } from "../apiService";
import '../styles/CreateGameForm.css';

function CreateGameForm({goBackFunc}) {
    const [inputName, setInputName] = useState('');
    const [inputPlayers, setInputPlayers] = useState(2);

    const handleCreateGame = async () => {
        try{
            const data = await create_game(inputName, inputPlayers, sessionStorage.getItem('playerId'));
        }
        catch(err){
            console.error(err);
        }
    }

    return (
        <div className="createGameForm">
        <h1>Crear sala</h1>
        <form>
            <div className="cgform-entry">
                <label> Nombre de la sala:
                    <input type='text' 
                    placeholder="Ingrese nombre"
                    maxLength={16}  
                    onChange={(e) => setInputName(e.target.value)}></input>
                </label>
            </div>
            <div className="cgform-entry">
                <label>
                    Jugadores:
                    <select onChange={(e) => setInputPlayers(e.target.value)}>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                    </select>
                </label>
            </div>
        </form>
        <div>
            <button className='green-button' onClick={() => goBackFunc(false)}>Volver</button>
            <button className='green-button' onClick={handleCreateGame}>Crear</button>
        </div>
        </div>
    );
}

export default CreateGameForm;