import React from "react"

import KillerIcon from "../../../public/player/killer-icon.svg"
import SurvivorIcon from "../../../public/player/survivor-icon.svg"
import HostIcon from "../../../public/player/host.png"
import ObsessionIcon from "../../../public/player/obsession.png"

export default function PlayerInfo({
    role,
    name,
    playerId,
    isSessionHost=false,
    isObsession=false,    
}) {

    return(
        <div className="PlayerInfo">
            <span className="PlayerInfo-icon">
                {role && role.toLowerCase() == "killer"
                ? <img src={KillerIcon} />
                : <img src={SurvivorIcon} />}
            </span>
            <div className="PlayerInfo-name-id">
                <div className="PlayerInfo-name-id-inner">
                    <span className="PlayerInfo-name">
                        {name
                        ? name
                        : "Player"}
                    </span>
                    <span className="PlayerInfo-id" >
                        {playerId
                        ? `#${playerId}`
                        : "#********"}
                    </span>
                </div>
            </div>
            {isSessionHost && <span className="PlayerInfo-host">
                <img src={HostIcon} title={`${name}#${playerId} is the Session host`} />
            </span>}
            {isObsession && <span className="PlayerInfo-obsession">
                <img src={ObsessionIcon} title={`${name}#${playerId} is the Obsession`} />
            </span>}            
        </div> 
    )
}

