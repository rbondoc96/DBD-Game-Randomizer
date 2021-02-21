import React from "react"
import {Link} from "react-router-dom"

export default function NavLink({
    href,
    children,
    isActive=false,
}) {

    return(
        <div className={isActive? "NavLink--active":"NavLink"}>
            <Link to={href}>
                {children}
            </Link>            
        </div>
    )
}