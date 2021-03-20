import React from "react"

import Icon from "../icon/Icon"
import UnknownSquare from "../../../public/player/unknown-square.png"

export default function PlayerResource({
    src,
    src2,
    src3,
    type,
    name,
    quote,
    rarities,
    description,
}) {

    let icon

    if(src) {
        // Resource is a Killer Power
        if(type && (type.toLowerCase() == "power")) {
            icon = <Icon 
                src={src}
                src2={src2}
                src3={src3}
                name={name}

                type="Power"

                description={description}
                quote={quote}
            />

        // Resource is Survivor Item
        } else if(rarities && (type && (type.toLowerCase() == "item"))) {
            icon = <Icon 
                src={src}
                name={name}

                rarities={rarities}
                type="Item"

                description={description}
                quote={quote}
            />
        } else {
            icon = <Icon src={UnknownSquare} />    
        }
    } else {
        icon = <Icon src={UnknownSquare} />
    }

    return(
        <div className="PlayerResource">
            {icon}
        </div>        
    )
}
