import React, {useState, useContext} from "react"
import {Redirect} from "react-router-dom"

import {SessionContext} from "../../context/SessionContext"

import TextInput from "../../components/inputs/TextInput"
import IconButton from "../../components/inputs/IconButton"
import JoinIcon from "../../../public/session/join.png"

export default function JoinSession() {

    const [session, setSession] = useContext(SessionContext)
    const [id, setId] = useState("")

    const handleClick = event => {
        const params = new URLSearchParams({
            "action": "join",
            "sessionId": id, 
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

    const handleTextInputChange = event => {
        setId(event.currentTarget.value)
    }

    return(
        <div className="Session-join">
            <h2>Join Existing Session</h2>

            <TextInput 
                label="Session ID"
                placeholder="ex. A1B3DD3"
                maxLength={6}
                value={id}
                onChange={handleTextInputChange}
            />

            <IconButton iconSrc={JoinIcon} text="Join Session" onClick={handleClick} />
        </div>
    )
}