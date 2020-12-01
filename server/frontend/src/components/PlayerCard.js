import React, {useContext, useState} from "react"

import {SessionContext} from "../context/SessionContext"

import Icon from "./Icon"
import Button from "./inputs/Button"
import TextInput from "./inputs/TextInput"
import SelectInput from "./inputs/SelectInput"
import CheckboxInput from "./inputs/CheckboxInput"

export default function PlayerCard({
    player,
    isHost,
}) {

    const [session, setSession] = useContext(SessionContext)
    const [formData, setFormData] = useState({
        action: "randomize",
        playerRole: "killer",
        noLicensedChars: false,
    })

    const onChange = event => {
        let self = event.currentTarget
        let name = self.getAttribute("name")
        let value = self.value

        if(self.getAttribute("type") == "checkbox")
            value = self.checked

        setFormData({
            ...formData,
            [name]: value,
        })
    }

    const onSubmit = event => {
        event.preventDefault()

        var url = event.currentTarget.getAttribute("action")
        var params = new URLSearchParams({
            playerId: session.playerId,
            ...formData,
        })

        fetch(url+"?"+params).then(res=>res.json()).then(json => {
            console.log(json)
        })
    }

    return(
        <div className="playerCard">
        {player && player["player_id"] == session.playerId && 
            <div className="playerCard-form-container">
                <form action="/api/player" onSubmit={onSubmit}>
                    <input 
                        type="hidden" 
                        defaultValue={formData.action} 
                        name="action"    
                    />
                    <SelectInput 
                        onChange={onChange}
                        value={formData.playerRole}
                        name="playerRole"
                        label="Select Role"
                    >
                        <option value="killer">Killer</option>
                        <option value="survivor">Survivor</option>
                    </SelectInput>
                    <CheckboxInput 
                        name="noLicensedChars"
                        onChange={onChange}
                        label="Non-licensed characters only?"
                    />    
                    <Button type="submit" children={"Randomize"} />
                </form>
            </div>}

            <div className="playerCard-header">
                <div>
                    <span>Player Name: </span>
                    <span>{player.name}</span>
                </div>
                <div>
                    <span>Player ID: </span>
                    <span className="playerCard-name">{player.player_id}</span>
                    {isHost && <span>HOST</span> && console.log(player)}
                </div>
            </div>
            <div className="playerCard-content">
                <div className="playerCard-character">
                    {player.character.image && <Icon 
                        src={player.character.image}
                        name={player.character.name}
                    />}
                </div>  
                <div className="playerCard-perks">
                    {player.perks.map(perk => {
                        return(<Icon 
                            src={perk["image"]}
                            name={perk["name"]}
                        />)
                    })}
                </div>   
                {player.role.toLowerCase() == "survivor" && 
                    <>
                        <div className="playerCard-item">
                            {player.item && <Icon 
                                src={player.item["image"]}
                                name={player.item["name"]}
                            />}
                        </div>
                        <div className="playerCard-offering">
                            {player.offering && <Icon 
                                src={player.offering["image"]}
                                name={player.offering["name"]}
                            />}
                        </div> 
                    </>               
                }
                {player.role.toLowerCase() == "killer" && 
                    <>
                        <div className="playerCard-power">
                            {player.power && <Icon 
                                src={player.power["image"]}
                                name={player.power["name"]}
                            />}
                        </div>
                        <div className="playerCard-offering">
                            {player.offering && <Icon 
                                src={player.offering["image"]}
                                name={player.offering["name"]}
                            />}
                        </div> 
                    </>
                }   
            </div>                                
        </div>
    )
}