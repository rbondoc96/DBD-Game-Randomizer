import React, {useContext} from "react"

import {UIContext} from "../../context/UIContext"
import {SessionContext} from "../../context/SessionContext"

import JoinSession from "./Join"
import CreateSession from "./Create"
import SessionRoom from "./Room"

import Page from "../../components/page/Page"

function SessionStart() {

    const {mobileState} = useContext(UIContext)
    const [isMobile, setIsMobile] = mobileState    

    const className = isMobile ? "SessionStart--mobile" : "SessionStart"

    return(
        <div className={className}>
            <CreateSession />
            <div className="SessionStart-vertical-line"></div>
            <JoinSession />
        </div>
    )
}

export default function Session() {

    const [session, setSession] = useContext(SessionContext)

    return(
        <Page classes={"overflow-y-initial"}>
            <div className="Session">
                {session && session.session_id
                ?   <SessionRoom />
                :   <SessionStart />
                }
            </div>
        </Page>
    )
}