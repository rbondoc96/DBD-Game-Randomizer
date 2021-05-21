import React, {useContext, useState, useEffect} from "react"

import {SelfContext} from "../../context/SelfContext"
import {SessionContext} from "../../context/SessionContext"

import Button from "../inputs/Button"
import CheckboxInput from "../inputs/CheckboxInput"

import PlayerInfo from "./PlayerInfo"
import PlayerCharacter from "./PlayerCharacter"
import PlayerPerks from "./PlayerPerks"
import PlayerResource from "./PlayerResource"
import PlayerAddons from "./PlayerAddons"
import PlayerOffering from "./PlayerOffering"
import PlayerStatList from "./PlayerStatList"

export default function Player({
    role,
    size,
    data,
    isSelf,
    isSessionHost,
    isObsession,
    buttonText="Randomize",
    buttonOnClick=null,
}) {
    const [session, setSession] = useContext(SessionContext)
    const [self, setSelf] = useContext(SelfContext)

    const [player, setPlayer] = useState(null)
    const [noLicensedChars, setNoLicensedChars] = useState(false)
    const [activeStatList, setActiveStatList] = useState(null)

    const toggleCharacterChoice = event => {
        let target = event.currentTarget
        setNoLicensedChars(target.checked)
    }

    const randomize = event => {
        var params
        if(role) {
            params = new URLSearchParams({
                "action": "randomize",
                "role": role,
                "noLicensedChars": noLicensedChars,
            })
        } else {
            params = new URLSearchParams({
                "action": "randomize",
                "noLicensedChars": noLicensedChars,
            })
        }

        fetch("/api/player/?" + params)
        .then(res => res.json())
        .then(json => {
            let data = json.player

            // Only if the acquired player is the current User
            if(self.player_id == data.player_id) {
                setSelf(data)
            }
            setPlayer(data)
        })

        /* Cleaning up button style */
        let button = event.currentTarget
        if(button.classList.contains("button--pulse")) {
            button.classList.remove("button--pulse")
        }
    }

    const statListOnClick = event => {
        let target = event.currentTarget
        if(target == activeStatList) {
            setActiveStatList(null)
        } else {
            setActiveStatList(target)
        }
    }    

    useEffect(() => {
        // Render prefetched data
        if(data) {
            setPlayer(data)
        }    
    }, [data])

    const headers = (player && player.role && player.role.toLowerCase() == "killer")
        ? ["Power", "Buffs", "Debuffs", "Tracking", "Special"] 
        : ["Item", "Buffs", "Debuffs", "Auras", "Special"]

    return(
        <div className="Player">    
            <PlayerInfo 
                isSessionHost={isSessionHost}
                isObsession={isObsession}
                role={(player && player.role)? player.role : role}
                name={player && player.name}
                playerId={player && player.player_id}
            />      
            <div className="Player-assets">
                {player && player.character
                ? <PlayerCharacter
                    name={player.character.name} 
                    src={player.character.image}
                />
                : <PlayerCharacter />
                }

                <div className="Player-resources">
                    {player
                    ? player.item
                        ? <PlayerResource 
                            src={player.item.overlay}
                            type="Item"
                            name={player.item.name}
                            quote={player.item.flavor}
                            rarities={player.item.rarities}
                            description={player.item.description}
                        />
                        : player.power
                            ? <PlayerResource 
                                src={player.power.primary_overlay}
                                src2={player.power.secondary_overlay}
                                src3={player.power.tertiary_overlay}
                                type="Power"
                                name={player.power.name}
                                quote={player.power.flavor}
                                description={player.power.description}
                            />
                            : <PlayerResource />
                    : <PlayerResource />
                    }
                    {player
                    ? player.item_addons.length > 0
                        ? <PlayerAddons 
                            addons={player.item_addons}
                        />
                        : player.power_addons.length > 0 
                            ? <PlayerAddons 
                                addons={player.power_addons}
                            />
                            : <PlayerAddons />
                    : <PlayerAddons />}
                </div>
                
                {player && player.offering 
                ? <PlayerOffering 
                    src={player.offering.overlay}
                    name={player.offering.name}
                    rarities={player.offering.rarities}
                    description={player.offering.description}
                    quote={player.offering.flavor}
                />
                : <PlayerOffering />
                }
    
                {player && player.perks 
                ? <PlayerPerks 
                    perks={player.perks}
                />
                : <PlayerPerks />
                }

                {isSelf && <div className="Player-checkbox">
                    <CheckboxInput 
                        id={"no-licensed-chars"}
                        name={"no-licensed-chars"}
                        label={"Free characters only?"}
                        onChange={toggleCharacterChoice}
                    />
                </div>}

                <div className="Player-button">
                    {isSelf
                    ? <button className="button" onClick={randomize}>
                        Randomize
                    </button>
                    
                    : isSessionHost 
                    ? <button className="button" onClick={buttonOnClick}>
                        {buttonText}
                    </button>
                    : ""}
                </div>
            </div>
            {/* To add later <div className="Player-stats">
                <h3 className="Player-stats-header">Player Stats</h3>
                <div className="Player-statlists">
                    {headers.map(str => {
                        return <PlayerStatList 
                            header={str}
                            onClick={statListOnClick}
                            activeStatList={activeStatList}
                        />
                    })}
                </div>
            </div> */}
        </div>        
    )
}