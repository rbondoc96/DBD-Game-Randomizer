import React, {createContext, useState} from "react"

export var initialState = {
    isLarge: window.innerWidth > 1000,
    isMedium: window.innerWidth <= 1000 && window.innerWidth > 650,
    isSmall: window.innerWidth <= 650,
}

export const ViewContext = createContext()

export function ViewProvider({children}) {
    
    const [view, setView] = useState({
        isLarge: window.innerWidth > 1000,
        isMedium: window.innerWidth <= 1000 && window.innerWidth > 650,
        isSmall: window.innerWidth <= 650,
    })

    return(
        <ViewContext.Provider value={[view, setView]}>
            {children}
        </ViewContext.Provider>
    )
}