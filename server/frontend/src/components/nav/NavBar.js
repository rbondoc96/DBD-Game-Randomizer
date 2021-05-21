import React, {useContext, useState, useEffect} from "react"
import {Link, useLocation, useRouteMatch} from "react-router-dom"

import {ViewContext} from "../../context/ViewContext"
import {UIContext} from "../../context/UIContext"

import NavLink from "./NavLink"

import Logo from "../../../public/logo.svg"

export default function NavBar({

}) {

    const [view, setView] = useContext(ViewContext)
    const {mobileState, navToggle} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState
    const [showNavToggle, setShowNavToggle] = navToggle

    const [showNavBar, setShowNavBar] = useState(false)

    const location = useLocation()
    const currentPath = location.pathname   

    const navbarToggle = event => {
        setShowNavBar(!showNavBar)
    }

    const resetNavbar = event => {
        if(window.innerWidth >= 950) {
            setShowNavBar(false)
        }
    }

    const hideMobileNavbar = event => {
        setShowNavBar(false)
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
            ? `NavBar--mobile${showNavBar
                ? ""
                : "--hidden"}`
            : "NavBar"}>
            <div className="NavBar-left">
                <NavLink 
                    href="/"
                    children="Home" 
                    onClick={hideMobileNavbar}
                    isActive={currentPath == "/"} 
                />
                <NavLink
                    href="/about"
                    children="About" 
                    onClick={hideMobileNavbar}
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
                    onClick={hideMobileNavbar}
                    isActive={currentPath.includes("/sessions")} 
                />
                <NavLink 
                    href="/settings"
                    children="Settings" 
                    onClick={hideMobileNavbar}
                    isActive={currentPath.includes("/settings")}     
                />
            </div>
        </div>
        {isMobile && <span 
            className={`NavBar-toggle${showNavToggle? "":" NavBar-toggle--hidden"}`}
            onClick={navbarToggle}
        >
            <svg viewBox="0 0 100 80" width="32" height="32">
                <rect width="100" height="10"></rect>
                <rect y="30" width="100" height="10"></rect>
                <rect y="60" width="100" height="10"></rect>
            </svg>
        </span>}
        </>
    )
}