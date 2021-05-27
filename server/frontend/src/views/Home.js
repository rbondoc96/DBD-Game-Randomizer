import React, {useRef, useState, useContext, useEffect} from "react"

import {UIContext} from "../context/UIContext"
import {SelfContext} from "../context/SelfContext"

import Player from "../components/player/Player"

import Page from "../components/page/Page"

function HomeRadioText({
    name,
    id,
    role,
    children,
    value,
    onClick,
}) {

    const {mobileState} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState    

    let labelClass
    if((role == value) && isMobile) {
        labelClass="HomeRadioText-label--mobile--active"
    } else if((role == value) && !isMobile) {
        labelClass="HomeRadioText-label--active"
    } else if((role != value) && isMobile) {
        labelClass="HomeRadioText-label--mobile"
    } else if((role != value) && !isMobile) {
        labelClass="HomeRadioText-label"
    }

    return(
        <div className="HomeRadioText">
            <label htmlFor={id} 
                className={labelClass}
            >
                {children}
                <input
                    checked={role==value}
                    id={id}
                    type="radio" 
                    name={name}
                    value={value}
                    onClick={onClick}   
                />
            </label>
        </div>
    )
}

export default function Home() {
    const [self, setSelf] = useContext(SelfContext)
    const {mobileState} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState
    const [role, setRole] = useState(null)

    const homeRadioOnClick = event => {
        let target = event.currentTarget
        let button = document.querySelector(
            ".Home .Player .Player-button .button"
        )
        if(target.checked) {
            setRole(target.getAttribute("value"))

            button.classList.add("button--pulse")
        }
    }

    useEffect(() => {
        if(self && self.role) {
            setRole(self.role.toLowerCase())
        } else {
            setRole("killer")
        }
    }, [self])
    
    return(
        <Page classes={"overflow-y-initial"}>
        <div className="Home">
            <div className="Home-randomizer">
                <Player 
                    role={role} 
                    data={self}
                    isSelf={true}
                />
            </div>
            <div className={
                isMobile? "Home-randomizer-options--mobile": "Home-randomizer-options"
                }>
                <HomeRadioText
                    onClick={homeRadioOnClick} 
                    value="killer"
                    name="killer-option"
                    id="killer-option"
                    role={role}
                    children="Killer"
                />
                <div className="Home-randomizer-vertical-separator"></div>
                <HomeRadioText 
                    onClick={homeRadioOnClick}
                    value="survivor"
                    name="survivor-option"
                    id="survivor-option"
                    role={role}
                    children="Survivor"
                />
            </div>
        </div>
    </Page>
    )
}