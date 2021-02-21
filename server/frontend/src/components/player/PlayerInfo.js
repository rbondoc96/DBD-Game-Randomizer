import React from "react"

import KillerIcon from "../../../public/player/killer-icon.svg"
import SurvivorIcon from "../../../public/player/survivor-icon.svg"

export default function PlayerInfo({
    role,
    name,
    playerId,
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
        </div> 
    )
}

