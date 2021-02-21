import React from "react"

// Default Player Character image
import UnknownCharacter from "../../../public/player/unknown-character.png"

export default function PlayerCharacter({
    src,
    name,
}) {
    return(
        <div className="PlayerCharacter">
            <div className="PlayerCharacter-image">
                <img src={src? src : UnknownCharacter} />
            </div>
            <div className="PlayerCharacter-name">
                <span>{name? name : "Unknown"}</span>
            </div>
        </div>
    )
}