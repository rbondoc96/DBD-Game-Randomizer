import React, {createContext, useState} from "react"

export const UIContext = createContext()

export function UIProvider({children}) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 960)
    const [showNavToggle, setShowNavToggle] = useState(true)

    return(
        <UIContext.Provider value={{
            mobileState: [isMobile, setIsMobile],
            navToggle: [showNavToggle, setShowNavToggle],
        }}>
            {children}
        </UIContext.Provider>
    )
}