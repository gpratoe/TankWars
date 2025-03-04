import React, { useState } from "react";
import { create_game } from "../apiService";
import '../styles/CreateGameForm.css';
import { useNavigate } from 'react-router-dom';
import Button from "./Button";

function CreateGameForm({goBackFunc}) {
    const [inputName, setInputName] = useState('');
    const [inputPlayers, setInputPlayers] = useState(4);
    const navigate = useNavigate();

    const handleCreateGame = async () => {
        try{
            const data = await create_game(inputName, inputPlayers, sessionStorage.getItem('playerId'));
            if (data && data.id) {
                sessionStorage.setItem('lobbyId', data.id);
                sessionStorage.setItem('playerColor', 'red');
                navigate(`/lobby/${data.id}`);
            }
            else{
                throw new Error('No se pudo obtener el id de la sala');
            }
        }
        catch(err){
            console.error(err);
        }
    }

    return (
        <>
            <h1>Crear sala</h1>
            <div className="createGameForm">
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
                            <select onChange={(e) => setInputPlayers(e.target.value)} defaultValue="4">
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>
                            </select>
                        </label>
                    </div>
                </form>
                <div>
                    <Button text='Volver' variant='red' onClick={() => goBackFunc(false)}/>
                    <Button text='Crear' onClick={handleCreateGame}/>
                </div>
            </div>
        </>
    );
}

export default CreateGameForm;