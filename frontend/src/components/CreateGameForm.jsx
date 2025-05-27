import React, { useState } from "react";
import { create_game } from "../apiService";
import '../styles/CreateGameForm.css';
import { useNavigate } from 'react-router-dom';
import Button from "./Button";
import { usePlayer } from "./contexts/playerContext";

function CreateGameForm({goBackFunc}) {
    const [inputName, setInputName] = useState('');
    const [inputPlayers, setInputPlayers] = useState(4);
    const { player, updatePlayer } = usePlayer();
    const navigate = useNavigate();

    const handleCreateGame = async () => {
        try{
            const data = await create_game(inputName, inputPlayers, player.id);
            if (data && data.id) {
                updatePlayer({ id: player.id, name: player.name, is_owner: true });
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

    const handleSubmit = (e) => {
        e.preventDefault(); 
        handleCreateGame(); 
    };

    return (
        <>
            <h1>Crear sala</h1>
            <div className="createGameForm">
                <form onSubmit={handleSubmit}>
                    <div className="cgform-entry">
                        <label> Nombre de la sala:</label>
                        <input type='text' 
                        placeholder="Ingrese nombre"
                        maxLength={16}  
                        onChange={(e) => setInputName(e.target.value)}>
                        </input>
                    </div>
                    <div className="cgform-entry">
                        <label>
                            Jugadores:
                        </label>
                        <select onChange={(e) => setInputPlayers(e.target.value)} defaultValue="4">
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                        </select>
                    </div>
                </form>
                <div className='button-container'>
                    <Button text='Volver' variant='red' onClick={() => goBackFunc(false)} type='button'/>
                    <Button text='Crear' onClick={handleCreateGame} type='submit'/>
                </div>
            </div>
        </>
    );
}

export default CreateGameForm;
