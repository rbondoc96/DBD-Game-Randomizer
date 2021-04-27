import React, {useState, useContext} from "react"
import {useRouteMatch} from "react-router-dom"

import {SessionContext} from "../../context/SessionContext"

import SelectInput from "../../components/inputs/SelectInput"
import IconButton from "../../components/inputs/IconButton"
import CreateIcon from "../../../public/session/create.png"

export default function CreateSession() {
    const [session, setSession] = useContext(SessionContext)    
    const [mode, setMode] = useState("survivor")

    const handleClick = event => {
        const params = new URLSearchParams({
            "action": "create",
            "mode": mode, 
        })

        fetch("/api/session/?" + params)
        .then(res => res.json())
        .then(json => {
            if(!json.error) {
                console.log(json)                
                setSession(json.session)
            } else {
                console.error(json)
            }
        })       
    }

    const handleModeChange = event => {
        setMode(event.currentTarget.value)
    }

    return(
        <div className="Session-create">
            <h2>Create New Session</h2>

            <SelectInput 
                label="Session Mode"
                onChange={handleModeChange}
                children={
                    <>
                        <option value="survivor">Survive with Friends</option>
                        <option value="custom">Custom Game</option>
                    </>
                }
            />

            <IconButton iconSrc={CreateIcon} text="Create Session" onClick={handleClick} />
        </div>    
    )
}