import React, {useEffect, useContext} from "react"

import {UIContext} from "../../context/UIContext"
import {SelfContext} from "../../context/SelfContext"
import {SessionContext} from "../../context/SessionContext"

import Player from "../../components/player/Player"

import UnknownRealm from "../../../public/session/unknown-realm.png"

export default function SessionRoom() {
    const tag = "[SessionRoom]"
    const {mobileState} = useContext(UIContext)
    const [isMobile] = mobileState

    const [self, setSelf] = useContext(SelfContext)
    const [session, setSession] = useContext(SessionContext)

    useEffect(() => {
        const wsUrl = `ws://${window.location.host}/ws/session/${session.session_id}/`        
        const websocket = new WebSocket(wsUrl)

        websocket.onopen = () => {
            console.log(tag, "Successfully connected to Session", session.session_id)
        }

        websocket.onmessage = event => {
            let data = JSON.parse(event.data)
            console.log(data.session)

            setSession({
                ...(data.session),
                isConnected: true,
            })                
        }

        websocket.onclose = () => {
            console.log("onclose event")
            setSession({
                isConnected: false,
            })
            console.error("Websocket disconnected.")                
        }

        websocket.onerror = error => {
            console.error("Error occurred:", error)
        }

        setSession({
            ...session,
            isConnected: true,
        })

        return () => {
            websocket.close()
            setSession({
                isConnected: false,
            })
        }

    }, [])

    return(
        <div className={isMobile? "SessionRoom--mobile" : "SessionRoom"}>
            <div className="SessionRoom-meta">
                <div className="SessionRoom-left">
                    <img className="SessionRoom-image"
                    src={session.realm? session.realm.image : UnknownRealm} />
                </div>
                <div className="SessionRoom-right">
                    <div className="SessionRoom-id">
                        <div className="SessionRoom-id-label">Session ID</div>
                        <div className="SessionRoom-id-value">{session.session_id}</div>
                    </div>
                    <div className="SessionRoom-mode">
                        <div className="SessionRoom-mode-label">Game Mode</div>
                        <div className="SessionRoom-mode-value">{session.mode}</div>
                    </div>
                    <div className="SessionRoom-host">
                        <div className="SessionRoom-host-label">Session Host</div>
                        <div className="SessionRoom-host-value">{session.host.name} <span>#{session.host.player_id}</span></div>
                    </div>
                    <div className="SessionRoom-obsession">
                        <div className="SessionRoom-obsession-label">Obsession</div>
                        <div className="SessionRoom-obsession-value">{session.obsession? <>
                            {session.obsession.name} <span>#{session.obsession.player_id}</span>
                        </> : "???"}</div>
                    </div>                                          
                    <div className="SessionRoom-realm">
                        <div className="SessionRoom-realm-name">{session.realm? session.realm.name : "Unknown Realm"}</div>
                    </div>
                </div>
            </div>
            <div className="SessionRoom-Players">
                {session.players && session.players.slice(0, 2) && session.players.slice(0, 2).map(elem => {
                    let isSessionHost = session.host.player_id == elem.player_id
                    
                    let isObsession = false
                    if(session.obsession && (session.obsession.player_id == elem.player_id))
                        isObsession = true

                    return(<div className="SessionRoom-Player">
                        <Player 
                            data={elem}
                            isSessionHost={isSessionHost}
                            isObsession={isObsession}
                        />
                    </div>)
                })}
            </div>
            <div className="SessionRoom-Players">
                {session.players && session.players.slice(2, 4) && session.players.slice(2, 4).map(elem => {
                    let isHost = self.player_id == elem.player_id
                    
                    return(<div className="SessionRoom-Player">
                        <Player 
                            data={elem}
                            isSessionHost={isSessionHost}
                            isObsession={isObsession}
                        />
                    </div>)
                })}
            </div>
            <div className="SessionRoom-Players">
                {session.players && session.players.slice(4) && session.players.slice(4).map(elem => {
                    let isHost = self.player_id == elem.player_id
                    
                    return(<div className="SessionRoom-Player">
                        <Player 
                            data={elem}
                            isSessionHost={isSessionHost}
                            isObsession={isObsession}
                        />
                    </div>)
                })}
            </div>                        
        </div>
    )
}