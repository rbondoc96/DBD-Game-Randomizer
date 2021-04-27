import React, {createContext, useState} from "react"

export const UIContext = createContext()

export function UIProvider({children}) {

    const [isMobile, setIsMobile] = useState(window.innerWidth < 960)

    return(
        <UIContext.Provider value={{
            mobileState: [isMobile, setIsMobile],
        }}>
            {children}
        </UIContext.Provider>
    )
}