import regeneratorRuntime from "regenerator-runtime"

import React, {useContext, useEffect, useState} from "react"
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"

import {ViewContext} from "./context/ViewContext"
import {SelfContext} from "./context/SelfContext"
import {GameContext} from "./context/GameContext"
import {PlayerContext} from "./context/PlayerContext"
import {SessionContext} from "./context/SessionContext"

// Styles
import "./styles/theme.scss"
import "./styles/views/home.scss"
import "./styles/views/session.scss"
import "./styles/components/nav.scss"
import "./styles/components/icon.scss"
import "./styles/components/inputs.scss"
import "./styles/components/player.scss"
import "./styles/components/scrollbar.scss"


// Views
import Home from "./views/Home"
import Join from "./views/Join"
import Create from "./views/Create"
import Session from "./views/Session"

import NavBar from "./components/nav/NavBar"

import IconWindow from "./components/icon/IconWindow"

export default function App(props) {

    const [view, setView] = useContext(ViewContext)
    // const [game, setGameContext] = useContext(GameContext)
    // const [player, setPlayer] = useContext(PlayerContext)
    // const [session, setSession] = useContext(SessionContext)

    const resizeHandler = () => {
        setView({
            isLarge: window.innerWidth > 950,
            isMedium: window.innerWidth <= 950 && window.innerWidth > 650,
            isSmall: window.innerWidth <= 650,
        })
    }

    useEffect(() => {
        window.addEventListener("resize", resizeHandler)
    
        return () => {
            window.removeEventListener("resize", resizeHandler)
        }
    }, [])

    return(
        <>
            <Router>
                <div className="app">
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route path="/join" component={Join} />
                    <Route path="/create" component={Create} />
                    <Route path="/session" component={Session} />
                </Switch>
                {/* <IconWindow 
                /> */}
                <NavBar />
                </div>
            </Router>
        </>
    )
}