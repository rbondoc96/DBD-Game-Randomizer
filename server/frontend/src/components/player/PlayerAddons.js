import React from "react"

import Icon from "../icon/Icon"
import UnknownSquare from "../../../public/player/unknown-square.png"

export default function PlayerAddons({
    addons,
}) {
    var addonNodes = []

    if(addons) {
        for(let i=0; i<addons.length; i++) {
            let addon = addons[i]
            addonNodes.push(<Icon
                size="small"
                src={addon.overlay} 
                name={addon.name}
                
                rarities={addon.rarities}
                reference={addon.power
                ? addon.power.name
                : addon.type
                    ? addon.type
                    : ""
                }
                type="Add-On"

                description={addon.description}
                effects={addon.effects}
            />)
        }
    }

    // Fill in any missing addons
    while(addonNodes.length != 2) {
        addonNodes.push(<Icon 
            size="small"
            src={UnknownSquare}
        />)
    }


    return(
        <div className="PlayerAddons">
            <div className="Player-addon">
                {addonNodes[0]}
            </div>

            <div className="Player-plus-sign">+</div>

            <div className="Player-addon">
                {addonNodes[1]}
            </div>
        </div>
    )
}