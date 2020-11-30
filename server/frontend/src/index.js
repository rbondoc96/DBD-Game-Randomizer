import React from "react"
import ReactDOM from "react-dom"

import {GameProvider} from "./context/GameContext"
import {PlayerProvider} from "./context/PlayerContext"
import {SessionProvider} from "./context/SessionContext"

import App from "./app"

ReactDOM.render(
    <React.StrictMode>
        <GameProvider>
            <SessionProvider>
                <PlayerProvider>
                    <App />
                </PlayerProvider>
            </SessionProvider>
        </GameProvider>
    </React.StrictMode>, 
    document.getElementById("root")
)