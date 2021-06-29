import regeneratorRuntime from "regenerator-runtime"
import throttle from "lodash/throttle"

import React, {useContext, useEffect, useState} from "react"
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"

import {UIContext} from "./context/UIContext"
import {SelfContext} from "./context/SelfContext"
import {SessionProvider} from "./context/SessionContext"

import "./styles/theme.css"
import "./styles/views/_all.css"
import "./styles/components/_all.css"

import Home from "./views/Home"
import About from "./views/About"
import Session from "./views/session/Session"
import Settings from "./views/Settings"

import NavBar from "./components/nav/NavBar"
import IconWindow from "./components/icon/IconWindow"

export default function App(props) {

    const [self, setSelf] = useContext(SelfContext)
    const {mobileState, navToggle} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState
    const [showNavToggle, setShowNavToggle] = navToggle


    var prevScrollPos = window.pageYOffset
    const onScroll = event => {
        var currScrollPos = window.pageYOffset

        if(prevScrollPos > currScrollPos) {
            setShowNavToggle(true)
        } else {
            setShowNavToggle(false)
        }

        prevScrollPos = currScrollPos
    }     

    const handleResize = () => {
        setIsMobile(window.innerWidth < 960)
    }

    useEffect(() => {
        const throttledScroll = throttle(onScroll, 100)

        window.addEventListener("resize", handleResize)
        window.addEventListener("scroll", throttledScroll)

        if(self == null) {
            fetch("api/player/")
            .then(res => res.json())
            .then(json => {    
                setSelf(json.player)
            })
        }        
    
        return () => {
            window.removeEventListener("resize", handleResize)
            window.removeEventListener("scroll", throttledScroll)
        }
    }, [])

    let cssClass = !isMobile? "app":"app--mobile"

    return(
        <>
            <Router>
                <div className={cssClass}>
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route path="/about" component={About} />
                    <Route path="/sessions" render={() => (
                        <Session />
                    )}/>
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