import React, {useContext, useState, useEffect} from "react"
import {Link, useLocation} from "react-router-dom"

import {ViewContext} from "../../context/ViewContext"

import NavLink from "./NavLink"

import Logo from "../../../public/logo.svg"

export default function NavBar({

}) {

    const [view, setView] = useContext(ViewContext)
    const [showNavbar, setShowNavbar] = useState(false)

    const location = useLocation()
    const currentPath = location.pathname

    const navbarToggle = event => {
        setShowNavbar(!showNavbar)
    }

    // Hides navbar once the screen gets bigger
    const resetNavbar = event => {
        if(window.innerWidth >= 950) {
            setShowNavbar(false)
        }
    }

    useEffect(() => {
        
        window.addEventListener("resize", resetNavbar)

        return () => {
            window.removeEventListener("resize", resetNavbar)
        }
    }, [])
    
    return(
        <>
        <div className={(view.isMedium || view.isSmall)
            ? `NavBar--mobile${showNavbar
                ? ""
                : "--hidden"}`
            : "NavBar"}>
            <div className="NavBar-left">
                <NavLink 
                    href="/"
                    children="Home" 
                    isActive={currentPath == "/"} 
                />
                <NavLink
                    href="/about"
                    children="About" 
                    isActive={currentPath == "/about"} 
                />
            </div>
            <div className="NavBar-center">
                <Link to="/">
                    <img src={Logo} />
                </Link>
            </div>
            <div className="NavBar-right">
                <NavLink 
                    href="/sessions"
                    children="Sessions" 
                    isActive={currentPath == "/sessions"} 
                />
                <NavLink 
                    href="/settings"
                    children="Settings" 
                    isActive={currentPath == "/settings"}     
                />
            </div>
        </div>
        {(view.isMedium || view.isSmall) && <span 
            className="NavBar-toggle" 
            onClick={navbarToggle}
        >
        </span>}
        </>
    )
}