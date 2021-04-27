import React from "react"

export default function IconButton({
    iconSrc,
    text,
    onClick,
}) {

    return(
        <button className="IconButton" onClick={onClick} >
            <img src={iconSrc} />
            <span>{text}</span>
        </button>
    )
}