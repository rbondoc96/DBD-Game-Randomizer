import React, {useEffect, useContext} from "react"
import {Redirect} from "react-router-dom"

import {SessionContext} from "../context/SessionContext"

import Button from "../components/inputs/Button"
import PlayerCard from "../components/PlayerCard"

export default function Session({
    
}) {
    
    const [session, setSession] = useContext(SessionContext)
    var websocket = null

    const startSession = event => {
        console.log(session)
        // Send session data over websocket for validation
    }

    useEffect(() => {
        const wsUrl = `ws://${window.location.host}/ws/session/${session.sessionId}/`

        websocket = new WebSocket(wsUrl)            
        websocket.onopen = () => {
            console.log("Successfully connected to Session")

            if(session.playerName) {
                websocket.send(JSON.stringify({
                    playerName: session.playerName
                }))
            }
        }
        websocket.onmessage = event => {
            let data = JSON.parse(event.data)
            setSession({
                ...session,
                playerId: data["playerId"],
                sessionId: data["sessionId"],
                session: data["session"],
                isConnected: true,
            })                
        }
        websocket.onclose = () => {
            console.log("onclose event")
            setSession({
                ...session,
                session: null,
                sessionId: null,
                sessionUrl: null,
                isConnected: false,
            })
            console.error("Websocket disconnected.")                
        }
        websocket.onerror = error => {
            console.error("Error occurred:", error)
        }

        setSession({
            ...session,
            sessionUrl: wsUrl,
            isConnected: true,
        })

        return () => {
            websocket.close()
            setSession({
                ...session,
                sessionId: null,
                sessionUrl: null,
                session: null,
                websocket: null,
                isConnected: false,
            })
        }

    }, [])

    if(!session.sessionId) {
        return <Redirect to="/join" />
    } else {
        return(
            <>
            {session.session && <div className="Session">
                <div className="session-players">
                {session.session.players.map(player => {
                    return(<PlayerCard 
                        player={player}
                    />)
                })}
                </div>

                <div className="session-meta">
                    <div className="session-info">
                        <div>
                            Session ID: <span>{session.sessionId}</span>
                        </div>
                        <div>
                            Session Mode: <span>{session.session.mode}</span>
                        </div>
                    </div>                
                {session.playerId != session.session.host.playerId &&
                    <Button 
                        type="button" 
                        onClick={startSession} 
                        children={"Start Session"} 
                    />
                }
                </div>                
            </div>}
            </>
        )
    }
}