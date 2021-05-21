import React from "react"

import Icon from "../icon/Icon"
import UnknownPerk from "../../../public/player/unknown-perk.png"

export default function PlayerPerks({
    perks
}) {
    var perkNodes = []

    if(perks) {
        for(let i=0; i<perks.length; i++) {
            let perk = perks[i]
            perkNodes.push(<Icon
                src={perk.overlay} 
                name={perk.name}
                clickable={true}

                tiers={perk.tiers}
                rarities={perk.rarities}
                reference={perk.owner}
                type="Perk"

                quote={perk.flavor}
                description={perk.description}
                effects={perk.effects}
            />)
        }
    }

    // Fill in any missing perks
    while(perkNodes.length != 4) {
        perkNodes.push(<Icon 
            src={UnknownPerk}
        />)
    }

    return(
        <div className="PlayerPerks">
            <div className="Player-perkset">
                {perkNodes[0]}
                {perkNodes[1]}
            </div>
            <div className="Player-perkset">
                {perkNodes[2]}
                {perkNodes[3]}
            </div>
        </div>        
    )
}