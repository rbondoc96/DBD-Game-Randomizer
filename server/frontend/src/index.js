import React from "react"
import ReactDOM from "react-dom"

import {UIProvider} from "./context/UIContext"
import {SelfProvider} from "./context/SelfContext"
import {IconProvider} from "./context/IconContext"
import {SessionProvider} from "./context/SessionContext"


import App from "./app"

ReactDOM.render(
    <React.StrictMode>
        <UIProvider>
            <SessionProvider>
                <SelfProvider>
                    <IconProvider>
                        <App />
                    </IconProvider>
                </SelfProvider>
            </SessionProvider>
        </UIProvider>
    </React.StrictMode>, 
    document.getElementById("root")
)