import React, {createContext, useState} from "react"

export const IconContext = createContext()

export function IconProvider({
    children
}) {
    // The current active Icon component
    const [icon, setIcon] = useState()

    return(
        <IconContext.Provider value={[icon, setIcon]}>
            {children}
        </IconContext.Provider>
    )
}