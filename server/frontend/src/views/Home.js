import React, {useRef} from "react"

import RouterButton from "../components/inputs/RouterButton"

export default function Home() {
    
    return(
        <div className="Home">
            <RouterButton 
                type="button"
                to="/join"
                children={"Join an Existing Session"}
            />
            <RouterButton 
                type="button"
                to="/create"
                children={"Create a New Session"}
            />
        </div>
    )
}