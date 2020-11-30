import React from "react"
import {Link} from "react-router-dom"

export default function RouterButton({
    id,
    onClick,
    to,
    type="button",
    children,
}) {

    return(
        <div className="Button">
            {to
            ? <Link to={to}>
                <button type={type} id={id} onClick={onClick}>
                    {children}
                </button>
            </Link>
            : <button type={type} id={id} onClick={onClick}>
                {children}
            </button>}
        </div>
    )
}