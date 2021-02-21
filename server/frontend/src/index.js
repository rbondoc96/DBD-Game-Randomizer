import React from "react"
import ReactDOM from "react-dom"

import {ViewProvider} from "./context/ViewContext"
import {SelfProvider} from "./context/SelfContext"
import {IconProvider} from "./context/IconContext"
import {GameProvider} from "./context/GameContext"
import {PlayerProvider} from "./context/PlayerContext"
import {SessionProvider} from "./context/SessionContext"

import App from "./app"

ReactDOM.render(
    <React.StrictMode>
        <GameProvider>
            <SessionProvider>
                <PlayerProvider>
                    <ViewProvider>
                        <SelfProvider>
                            <IconProvider>
                                <App />
                            </IconProvider>
                        </SelfProvider>
                    </ViewProvider>
                </PlayerProvider>
            </SessionProvider>
            </GameProvider>
    </React.StrictMode>, 
    document.getElementById("root")
)