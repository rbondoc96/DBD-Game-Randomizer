import React from "react";
import {Link} from "react-router-dom"

export default function HomeButton({
    id,
    onClick,
    to,
    icon,
    type="button",
    children,
}) {

    return(
        <div className="HomeButton">
            {to
            ? <Link to={to}>
                <button type={type} id={id} onClick={onClick}>
                    {icon && <img src={icon} />}
                    <div>{children}</div>
                </button>
            </Link>
            : <button type={type} id={id} onClick={onClick}>
                {icon && <img src={icon} />}
                <div>{children}</div>
            </button>}
        </div>
    )
}