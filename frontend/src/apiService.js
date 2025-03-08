import axios from 'axios';

export const API_URL = 'http://localhost:8000';

export async function create_player(name) {
    try{
      const response = await axios.post(`${API_URL}/player?name=${name}`)
      if(response.status === 201){
        return response.data;
      }
      else {
        throw new Error(`Error al crear el jugador: ${response.statusText}`);
      }
    }
    catch (error){
      throw new Error(`Error al crear el jugador: ${error.message}`);
    }
  }

export async function get_lobbies() {
    try{
        const response = await axios.get(`${API_URL}/game?lobby=true`);
        if (response.status === 200){
            return response.data;
        }
        else {
            throw new Error(`Error al obtener las partidas: ${response.statusText}`);
        }
    }
    catch (error){
        throw new Error(`Error al obtener las partidas: ${error.message}`);
    }
}

export async function join_game(lobby_id, player_id) {
    try{
        const response = await axios.post(`${API_URL}/game/${lobby_id}/players?player_id=${player_id}`);
        if (response.status === 202){
            return response.data;
        }
        else {
            throw new Error(`Error al unirse a la partida: ${response.statusText}`);
        }
    }
    catch (error){
        throw new Error(`Error al unirse a la partida: ${error.message}`);
    }
}

export async function create_game(name, max_players, owner_id) {
    try{
        const body = {
            name: name,
            max_players: max_players,
            owner_id: owner_id
        }
        const response = await axios.post(`${API_URL}/game`, body);
        if (response.status === 201){
            return response.data;
        }
        else {
            throw new Error(`Error al crear la partida: ${response.statusText}`);
        }
    }
    catch (error){
        throw new Error(`Error al crear la partida: ${error.message}`);
    }
}

export async function get_game_players(lobby_id) {
    try{
        const response = await axios.get(`${API_URL}/game/${lobby_id}/players`);
        if (response.status === 200){
            return response.data;
        }
        else {
            throw new Error(`Error al obtener los jugadores: ${response.statusText}`);
        }
    }
    catch (error){
        throw new Error(`Error al obtener los jugadores: ${error.message}`);
    }
}

export async function leave_lobby(lobby_id, player_id) {
    try{
        const response = await axios.delete(`${API_URL}/game/${lobby_id}/players/${player_id}`);
        if (response.status === 202){
            return response.data;
        }
        else {
            throw new Error(`Error al abandonar la partida: ${response.statusText}`);
        }
    }
    catch (error){
        throw new Error(`Error al abandonar la partida: ${error.message}`);
    }
}

export async function start_game(lobby_id, owner_id) {
    try{
        const response = await axios.post(`${API_URL}/game/${lobby_id}/start?owner_id=${owner_id}`);
        if (response.status === 202){
            return response.data;
        }
        else {
            throw new Error(`Error al iniciar la partida: ${response.statusText}`);
        }
    }
    catch (error){
        throw new Error(`Error al iniciar la partida: ${error.message}`);
    }
}