import React, {useRef, useState, useContext, useEffect} from "react"

import {ViewContext} from "../context/ViewContext"
import {SelfContext} from "../context/SelfContext"

import Player from "../components/player/Player"

function HomeRadioText({
    name,
    id,
    role,
    children,
    value,
    onClick,
}) {

    return(
        <div className="HomeRadioText">
            <label htmlFor={id} 
                className={role==value
                    ? "HomeRadioText-label--active"
                    : "HomeRadioText-label"
                }
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
    const [view, setView] = useContext(ViewContext)
    const [self, setSelf] = useContext(SelfContext)
    const [role, setRole] = useState(null)

    const homeRadioOnClick = event => {
        let self = event.currentTarget
        if(self.checked) {
            setRole(self.getAttribute("value"))
        }
    }

    useEffect(() => {
        fetch("api/player/")
        .then(res => res.json())
        .then(json => {
            let player = json.player
            console.log(player)

            if(player.role) {
                setRole(json.player.role.toLowerCase())
            } else {
                setRole("killer")
            }

            setSelf(json.player)
        })
    }, [])
    
    return(
        <div className="Home">
            <div className="Home-randomizer">
                <Player size={
                    view.isLarge
                    ? "large"
                    : view.isMedium
                        ? "medium"
                        : "small"
                } 
                role={role} 
                data={self}
                />
            </div>
            <div className="Home-randomizer-options">
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
    )
}