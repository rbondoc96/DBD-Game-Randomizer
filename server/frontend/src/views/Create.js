import React, {useState, useContext} from "react"

import {SessionContext} from "../context/SessionContext"

import Button from "../components/inputs/Button"
import SelectInput from "../components/inputs/SelectInput"

export default function Create({

}) {

    const [session, setSession] = useContext(SessionContext)

    const onSubmit = event => {
        event.preventDefault()
        var self = event.currentTarget
        let url = self.getAttribute("action")
    }

    // useEffect(() => {

    // }, [])

    return(
        <div className="Create">
            <form method="GET" action="/api/session" onSubmit={onSubmit} >
                <SelectInput 
                    name="sessionType"
                    label="Session Type"
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