import React, {createContext, useState} from "react"

export const initialState = {
    playerId: null,
    playerName: null,
    sessionId: null,
    sessionUrl: null,
    session: null,
    isConnected: false,
}

export const SessionContext = createContext()

export function SessionProvider({
    children
}) {

    const [session, setSession] = useState(initialState)

    return(
        <SessionContext.Provider value={[session, setSession]}>
            {children}
        </SessionContext.Provider>
    )
}