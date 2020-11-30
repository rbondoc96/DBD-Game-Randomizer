import React from "react"

export default function Button({
    id,
    onClick,
    href,
    type="button",
    children,
}) {

    return(
        <div className="Button">
            {href
            ? <a href={href}>
                <button type={type} id={id} onClick={onClick}>
                    {children}
                </button>
            </a>
            : <button type={type} id={id} onClick={onClick}>
                {children}
            </button>}
        </div>
    )
}