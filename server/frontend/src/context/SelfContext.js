import React, {createContext, useState} from "react"

export const SelfContext = createContext()

export function SelfProvider({
    children
}) {
    const [self, setSelf] = useState()

    return(
        <SelfContext.Provider value={[self, setSelf]}>
            {children}
        </SelfContext.Provider>
    )
}