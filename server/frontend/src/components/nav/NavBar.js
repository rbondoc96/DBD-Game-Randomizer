import React, {useContext, useState, useEffect} from "react"
import {Link, useLocation, useRouteMatch} from "react-router-dom"

import {ViewContext} from "../../context/ViewContext"
import {UIContext} from "../../context/UIContext"

import NavLink from "./NavLink"

import Logo from "../../../public/logo.svg"

export default function NavBar({

}) {

    const [view, setView] = useContext(ViewContext)
    const {mobileState} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState

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
        <div className={isMobile
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
                    isActive={currentPath.includes("/about")} 
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
                    isActive={currentPath.includes("/sessions")} 
                />
                <NavLink 
                    href="/settings"
                    children="Settings" 
                    isActive={currentPath.includes("/settings")}     
                />
            </div>
        </div>
        {isMobile && <span 
            className="NavBar-toggle" 
            onClick={navbarToggle}
        >
        </span>}
        </>
    )
}