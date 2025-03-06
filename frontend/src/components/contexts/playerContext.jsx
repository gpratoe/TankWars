import { createContext, useContext, useState, useEffect } from "react";


export const PlayerContext = createContext(undefined);


export const PlayerProvider = ({ children }) => {

    const [player, setPlayer] = useState(() => {
        const storedPlayer = sessionStorage.getItem('player');
        return storedPlayer ? JSON.parse(storedPlayer) : { id: null, name: '', is_owner: false }; // handle page reloads
    });

  useEffect(() => {
    if (player && player.id !== null) { // handle page reloads
        sessionStorage.setItem('player', JSON.stringify(player));
    } else {
        sessionStorage.removeItem('player');
    }
  }, [player]);


    const updatePlayer = (newPlayerData) => {
        setPlayer({
            id: newPlayerData.id !== undefined ? newPlayerData.id : player.id,
            name: newPlayerData.name !== undefined ? newPlayerData.name : player.name,
            is_owner: newPlayerData.is_owner !== undefined ? newPlayerData.is_owner : player.is_owner,
        });
    };


    return (
        <PlayerContext.Provider value={{ player, setPlayer, updatePlayer }}>
            {children}
        </PlayerContext.Provider>
    );
};


export const usePlayer = () => {
    const context = useContext(PlayerContext);
    if (!context) {
        throw new Error("usePlayer must be used within a PlayerProvider");
    }
    return context;
};