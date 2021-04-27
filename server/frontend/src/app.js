import regeneratorRuntime from "regenerator-runtime"

import React, {useContext, useEffect, useState} from "react"
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"

import {ViewContext} from "./context/ViewContext"
import {SelfContext} from "./context/SelfContext"
import {GameContext} from "./context/GameContext"
import {PlayerContext} from "./context/PlayerContext"
import {SessionContext} from "./context/SessionContext"
import {UIContext} from "./context/UIContext"

// Styles
import "./styles/theme.scss"
import "./styles/views/_all.scss"
import "./styles/components/page/_all.scss"
import "./styles/components/inputs/_all.scss"
import "./styles/components/nav.scss"
import "./styles/components/icon.scss"
import "./styles/components/inputs.scss"
import "./styles/components/player.scss"
import "./styles/components/scrollbar.scss"


// Views
import Home from "./views/Home"
import About from "./views/About"
import Session from "./views/session/Session"
import Settings from "./views/Settings"

import NavBar from "./components/nav/NavBar"

import IconWindow from "./components/icon/IconWindow"

export default function App(props) {

    const [view, setView] = useContext(ViewContext)
    const {mobileState} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState
    const [self, setSelf] = useContext(SelfContext)

    // const [game, setGameContext] = useContext(GameContext)
    // const [player, setPlayer] = useContext(PlayerContext)
    // const [session, setSession] = useContext(SessionContext)

    const handleResize = () => {
        setIsMobile(window.innerWidth < 960)

        // setView({
        //     isLarge: window.innerWidth > 950,
        //     isMedium: window.innerWidth <= 950 && window.innerWidth > 650,
        //     isSmall: window.innerWidth <= 650,
        // })
    }

    useEffect(() => {
        window.addEventListener("resize", handleResize)

        if(self == null) {
            fetch("api/player/")
            .then(res => res.json())
            .then(json => {
                let player = json.player
                console.log("App call" , player)
    
                setSelf(json.player)
            })
        }        
    
        return () => {
            window.removeEventListener("resize", handleResize)
        }
    }, [])

    return(
        <>
            <Router>
                <div className="app">
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route path="/about" component={About} />
                    <Route path="/sessions" component={Session} />
                    <Route path="/settings" component={Settings} />
                </Switch>
                {/* <IconWindow 
                /> */}
                <NavBar />
                </div>
            </Router>
        </>
    )
}