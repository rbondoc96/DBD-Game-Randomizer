import React from "react"

import Icon from "../icon/Icon"

// Default Player Offering image
import UnknownOffering from "../../../public/player/unknown-offering.png"

export default function PlayerOffering({
    src,
    name,
    quote,
    rarity,
    description,
}) {
    
    return(
        <div className="PlayerOffering">
            {src
            ? <Icon 
                src={src}
                name={name}

                rarity={rarity}
                type="Offering"

                quote={quote}
                description={description}
            />

            : <Icon src={UnknownOffering} />                              
            } 
        </div>
    )
}
