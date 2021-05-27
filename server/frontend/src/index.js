import React from "react"
import ReactDOM from "react-dom"

import {UIProvider} from "./context/UIContext"
import {SelfProvider} from "./context/SelfContext"
import {IconProvider} from "./context/IconContext"


import App from "./app"

ReactDOM.render(
    <React.StrictMode>
        <UIProvider>
            <SelfProvider>
                <IconProvider>
                    <App />
                </IconProvider>
            </SelfProvider>
        </UIProvider>
    </React.StrictMode>, 
    document.getElementById("root")
)