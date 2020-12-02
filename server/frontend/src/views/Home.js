import React, {useRef} from "react"

import DbdImage from "../../public/dbd-logo.png"

import RouterButton from "../components/inputs/RouterButton"

export default function Home() {
    
    return(
        <div className="Home">
            <div className="Home-header">
                <img src={DbdImage} />
                <h1>Game Randomizer</h1>
            </div>
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