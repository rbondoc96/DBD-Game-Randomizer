import React, {useState, useContext, useRef} from "react"

import {GameContext} from "../context/GameContext"
import {SessionContext, connectTo} from "../context/SessionContext"

import Button from "./inputs/Button"

export default function GameForm({

}) {
    const numPlayersRef = useRef(null)
    const [game, setGameContext] = useContext(GameContext)
    const [session, setSession] = useContext(SessionContext)

    const [form, setForm] = useState({
        mode: "killer",
        numPlayers: 1,
        nonLicensedOnly: false,
        sessionId: null,
    })

    const connectTo = wsUrl => {
        return new Promise((resolve, reject) => {
            console.log("Connecting to websocket...")
    
            const sessionSocket = new WebSocket(wsUrl)
            sessionSocket.onopen = () => {
                console.log("Successfully connected to websocket.")
                resolve(sessionSocket)
            }
            sessionSocket.onerror = error => {
                reject(error)
            }
        })
    }    

    const onClick = event => {
        if(form.sessionId != session.sessionId && !session.websocket) {
            connectTo(`ws://${window.location.host}/ws/session/${form.sessionId}/`).then(sessionSocket => {

                sessionSocket.onmessage = event => {
                    console.log("onmessage")
                    let data = JSON.parse(event.data)
                    console.log(data)
                    setSession({
                        ...session,
                        playerId: data["playerId"],
                        sessionId: data["sessionId"],
                        session: data["session"],
                        isHost: data["isHost"],
                        isConnected: true,
                    })
                }
                sessionSocket.onclose = event => {
                    console.log("onclose")
                    setSession({
                        ...session,
                        session: null,
                        sessionId: null,
                        websocket: null,
                        isConnected: false,
                    })
                    console.error("Websocket disconnected.")
                }

                setSession({
                    ...session,
                    isConnected: true,
                    websocket: sessionSocket,
                }) 

                sessionSocket.send(JSON.stringify({
                    "message": `Client requesting: ${form.sessionId}`
                }))
                
                console.log("Message sent over socket")
                
            }).catch(error => {
                console.log("Error in connecting: ", error)
            })

        } else if(form.sessionId == session.sessionId && session.websocket) {
            console.log("Sending on existing connection...")

            // session.websocket.send(JSON.stringify({
            //     "message": "Please give me coke",
            // }))

        } else {
            console.log(form.sessionId)
            console.log(session.sessionId)
            console.log(session.websocket)
            console.log("No session ID provided.")
        }
        
    }

    const onChange = event => {
        var self = event.currentTarget
        var name = self.getAttribute("name")

        if(name == "mode") {
            let minPlayers = 1
            if(self.value == "custom") {
                minPlayers = 2
            } 

            numPlayersRef.current.value = minPlayers            
            setForm({
                mode: self.value,
                numPlayers: minPlayers,
            })
        } else if(self.getAttribute("type") == "checkbox") {
            setForm({
                ...form,
                [name]: self.checked
            })
        } else {
            setForm({
                ...form,
                [name]: self.value
            })
        }
    }

    const onSubmit = event => {
        event.preventDefault()
        
        let self = event.target
        let apiUrl = self.getAttribute("action")
        let params = new URLSearchParams({
            ...form
        })

        fetch(`${apiUrl}?${params}`)
        .then(res => res.json())
        .then(json => {
            console.log(json)
            setGameContext(json["session"])
        })
        .catch(res => console.log(res))
    }

    return(
        <div className="gameForm-container">
            <form method="GET" action="/api/session" onSubmit={onSubmit}>
                <label htmlFor="sessionId">Session Code</label>
                <input type="text" length="6" name="sessionId" id="sessionId" onChange={onChange}/>

                <label htmlFor="mode">Game Type</label>
                <select id="mode" name="mode" onChange={onChange} value={form.mode}>
                    <option value="killer">Killer (1 player)</option>
                    <option value="survivor">Survivor (1-4 players)</option>
                    <option value="custom">Custom Game (2-5 players)</option>
                </select>

                <label htmlFor="num-players">Number of Players</label>
                <select id="num-players" name="numPlayers" onChange={onChange} ref={numPlayersRef} value={form.numPlayers}>
                    {form.mode == "killer" &&
                        <option value="1">1</option>
                    }
                    {form.mode == "survivor" &&
                    <>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                    </>}
                    {form.mode == "custom" &&
                    <>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                    </>
                    }
                </select>             
                
                <label htmlFor="nonLicensedOnly">Non-Licensed Characters Only</label>
                <input type="checkbox" name="nonLicensedOnly" id="non-licensed-only" onChange={onChange} />
                <Button type="button" children="Test Websocket" id={"websocket"} onClick={onClick}/>
                <Button type="submit" children="Create a Session" />
            </form>
        </div>
    )
}