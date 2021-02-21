import React, {useState, useContext, useEffect} from "react"
import cookie from "react-cookies"

import {SessionContext} from "../context/SessionContext"

import Button from "../components/inputs/Button"
import SelectInput from "../components/inputs/SelectInput"

export default function Create({

}) {
    const [session, setSession] = useContext(SessionContext)

    const onChange = event => {
        let self = event.target
        let name = self.getAttribute("name")
        let value = self.value

        console.log(value)

        setSession({
            ...session,
            [name]: value,
        })
    }

    const onSubmit = event => {
        event.preventDefault()
        var self = event.currentTarget
        let url = self.getAttribute("action")
        let csrfcookie = cookie.load("csrftoken")

        let data = {
            ...session,
            csrfmiddlewaretoken: csrfcookie,
        }

        console.log("sending")

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(res => res.json())
        .then(json => {
            console.log(json)
        })
    }

    useEffect(() => {
        setSession({
            ...session,
            sessionId: null,
            sessionUrl: null,
            session: null,
            isConnected: false,
        })
    }, [])

    return(
        <div className="Create">
            <form method="GET" action="/api/session/" onSubmit={onSubmit} >
                <SelectInput 
                    name="sessionType"
                    label="Session Type"
                    onChange={onChange}
                >
                    <option value="killer">Killer</option>
                    <option value="survivor">Survivor</option>
                    <option value="custom">Kill Your Friends</option>
                </SelectInput>
                <Button type="submit" children={"Create Session"} />
            </form>
        </div>
    )
}