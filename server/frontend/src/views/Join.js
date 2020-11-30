import React, {useState, useContext, useEffect} from "react"
import {Redirect} from "react-router-dom"

import {SessionContext} from "../context/SessionContext"

import Button from "../components/inputs/Button"
import TextInput from "../components/inputs/TextInput"

export default function Join({

}) {

    const [session, setSession] = useContext(SessionContext)

    const [formData, setFormData] = useState({
        playerName: null,
        sessionId: null,
    })

    const onSubmit = event => {
        event.preventDefault()

        setSession({
            ...session,
            ...formData,
        })
    }

    useEffect(() => {
        setSession({
            ...session,
            sessionId: null,
            sessionUrl: null,
            session: null,
            websocket: null,
            isConnected: false,
        })
    }, [])

    const onChange = event => {
        let name = event.currentTarget.getAttribute("name")
        let value = event.currentTarget.value

        setFormData({
            ...formData,
            [name]: value,
        })
    }

    return(
        <>
        {!session.sessionId
        ?<div className="join">
            <form id="ws-form" onSubmit={onSubmit}>
                <TextInput 
                    label="Player Name"
                    id="player-name"
                    name="playerName"
                    onChange={onChange}
                />
                <TextInput 
                    label="Session Code"
                    id="session-id"
                    name="sessionId"
                    onChange={onChange}
                />
                <Button type="submit" children={"Join Session"} />
            </form>
        </div>
        :<Redirect to="/session" />
        }
        </>
    )
}