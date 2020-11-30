import React, {createContext, useState} from "react"

export const PlayerContext = createContext()

export function PlayerProvider({
    children
}) {
    const [player, setPlayer] = useState({
        playerId: null,
    })

    return(
        <PlayerContext.Provider value={[player, setPlayer]}>
            {children}
        </PlayerContext.Provider>
    )
}