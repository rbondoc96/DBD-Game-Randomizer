import React from "react"

// Default Player Character image
import UnknownCharacter from "../../../public/player/unknown-character.png"

export default function PlayerCharacter({
    src,
    name,
}) {
    let tokens = name 
        ? name.split(" ")
        : ["Unknown", "Character"]

    return(
        <div className="PlayerCharacter">
            <div className="PlayerCharacter-image">
                <img src={src? src : UnknownCharacter} />
            </div>
            <div className="PlayerCharacter-name">
                <span>
                    <div>
                        {tokens[0]}
                    </div>
                    <div>
                        {tokens.length == 3
                            ? `${tokens[1]} ${tokens[2]}`
                            : `${tokens[1]}`
                        }
                    </div>
                </span>
            </div>
        </div>
    )
}