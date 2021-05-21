import React from "react"
import {Link} from "react-router-dom"

export default function NavLink({
    href,
    children,
    onClick,
    isActive=false,
}) {

    return(
        <div className={isActive? "NavLink--active":"NavLink"}>
            <Link to={href} onClick={onClick}>
                {children}
            </Link>            
        </div>
    )
}