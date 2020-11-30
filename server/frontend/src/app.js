import React, {useContext, useEffect} from "react"
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"

import CharacterCard from "./components/CharacterCard"
import PlayerCard from "./components/PlayerCard"
import GameForm from "./components/GameForm"

import {GameContext} from "./context/GameContext"
import {PlayerContext} from "./context/PlayerContext"
import {SessionContext} from "./context/SessionContext"

import "./styles/theme.scss"
import "./styles/views.scss"
import "./styles/components.scss"
import "./styles/components/inputs.scss"
import "./styles/components/cards.scss"

// Partials
// import NavBar from "./components/navbar"
// import Footer from "./components/footer"

// Views
import Home from "./views/Home"
import Join from "./views/Join"
import Create from "./views/Create"
import Session from "./views/Session"

export default function App(props) {
    const [game, setGameContext] = useContext(GameContext)
    const [player, setPlayer] = useContext(PlayerContext)
    const [session, setSession] = useContext(SessionContext)

    return(
        <Router>
            <div className="app">
            <Switch>
                <Route exact path="/" component={Home} />
                <Route path="/join" component={Join} />
                <Route path="/create" component={Create} />
                <Route path="/session" component={Session} />
            </Switch>
            </div>
        </Router>
    )
}