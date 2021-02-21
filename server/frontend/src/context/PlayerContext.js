import React, {createContext, useState} from "react"

export const PlayerContext = createContext()

export function PlayerProvider({
    children
}) {
    const [player, setPlayer] = useState()

    return(
        <PlayerContext.Provider value={[player, setPlayer]}>
            {children}
        </PlayerContext.Provider>
    )
}