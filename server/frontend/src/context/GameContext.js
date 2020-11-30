import React, {createContext, useState} from "react"

export const GameContext = createContext()

export function GameProvider({children}) {
    const [game, setGameContext] = useState(null)

    return(
        <GameContext.Provider value={[game, setGameContext]}>
            {children}
        </GameContext.Provider>
    )
}