import React from "react"

import Icon from "./icon/Icon"

export default function CharacterCard({
    character,
}) {

    console.log(character)

    return(
        <div className="characterCard-container">
            <div className="characterCard-character">
                {character["character"]["image"] && <Icon 
                    src={character["character"]["image"]}
                    name={character["character"]["name"]}
                />}
            </div>
            <div className="characterCard-perks">
                {character["perks"].map(perk => {
                    return(<Icon 
                        src={perk["image"]}
                        name={perk["name"]}
                    />)
                })}
            </div>
            {character["role"].toLowerCase() == "survivor" && 
                <>
                    <div className="characterCard-item">
                        {character["item"] && <Icon 
                            src={character["item"]["image"]}
                            name={character["item"]["name"]}
                        />}
                    </div>
                    <div className="characterCard-offering">
                        {character["offering"] && <Icon 
                            src={character["offering"]["image"]}
                            name={character["offering"]["name"]}
                        />}
                    </div> 
                </>               
            }
            {character["role"].toLowerCase() == "killer" && 
                <>
                    <div className="characterCard-power">
                        {character["power"] && <Icon 
                            src={character["power"]["image"]}
                            name={character["power"]["name"]}
                        />}
                    </div>
                    <div className="characterCard-offering">
                        {character["offering"] && <Icon 
                            src={character["offering"]["image"]}
                            name={character["offering"]["name"]}
                        />}
                    </div> 
                </>
            }            
        </div>
    )
}