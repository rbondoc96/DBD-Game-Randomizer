import React, {useRef, useContext, useState, useEffect} from "react";

import {IconContext} from "../../context/IconContext"

import UncommonPerk from "../../../public/bgs/dsquare/uncommon-dsquare.png"
import RarePerk from "../../../public/bgs/dsquare/rare-dsquare.png"
import VeryRarePerk from "../../../public/bgs/dsquare/very-rare-dsquare.png"

import CommonSquare from "../../../public/bgs/square/common-square.png"
import UncommonSquare from "../../../public/bgs/square/uncommon-square.png"
import RareSquare from "../../../public/bgs/square/rare-square.png"
import VeryRareSquare from "../../../public/bgs/square/very-rare-square.png"
import UltraRareSquare from "../../../public/bgs/square/ultra-rare-square.png"
import EventSquare from "../../../public/bgs/square/event-square.png"

import CommonOffering from "../../../public/bgs/hex/common-hex.png"
import UncommonOffering from "../../../public/bgs/hex/uncommon-hex.png"
import RareOffering from "../../../public/bgs/hex/rare-hex.png"
import VeryRareOffering from "../../../public/bgs/hex/very-rare-hex.png"
import UltraRareOffering from "../../../public/bgs/hex/ultra-rare-hex.png"
import EventOffering from "../../../public/bgs/hex/event-hex.png"

const SIZES = ["small", "medium"]

export default function Icon({
    src,
    src2,
    src3,
    type,
    reference,
    name,
    tiers,
    rarities,
    description,
    quote,
    effects,
    size=SIZES[1]
}) {
    // Renaming to mainIcon to differentiate with the current instance
    const [mainIcon, setMainIcon] = useContext(IconContext)
    const [rarityIndex, setRarityIndex] = useState(null)
    const [filename, setFilename] = useState()

    const setAsMainIcon = event => {
        
        /*
        Toggle Window on Icon click

        In situations where the same Icon (basically has the same image/info) exists on the window, clicking a duplicate version of the Icon will
        STILL toggle the window.
        */
        if(mainIcon && (mainIcon.src == src)) {
            setMainIcon(null)
        } else {
            if(description != null) {
                setMainIcon({
                    src: src,
                    src2: src2,
                    src3: src3,
                    name: name,          
                    tier: tier,      
                    rarity: rarity,
                    reference: reference,
                    type: type,
                    description: description,
                    quote: quote,   
                    effects: effects,         
                })
            } else {
                setMainIcon(null)
            }
        }
    }

    const toggleRarities = event => {
        if(rarities && rarities.length == 1) {
            setRarityIndex(0)
            setFilename(getFilename(0))
        } else {
            if(rarityIndex >= 2) {
                setRarityIndex(0)
                setFilename(getFilename(0))
            } else {
                let newIndex = rarityIndex + 1
                setRarityIndex(newIndex)
                setFilename(getFilename(newIndex))
            }
        }   
    }

    const getFilename = rarityIndex => {
        var file = ""
        var type__lower = type ? type.toLowerCase() : null
        var rarity = rarities[rarityIndex]
        console.log(type__lower)
        if(rarity && type__lower) {
            switch(type__lower) {
                case "perk":
                    switch(rarity.toLowerCase()) {
                        case "uncommon":
                            file = UncommonPerk
                            break
                        case "rare":
                            file = RarePerk
                            break          
                        case "very rare":
                            file = VeryRarePerk
                            break  
                        default:
                            file = UncommonPerk
                            break
                    }
                    break

                case "item":
                    switch(rarity.toLowerCase()) {
                        case "common":
                            file = CommonSquare
                            break
                        case "uncommon":
                            file = UncommonSquare
                            break
                        case "rare":
                            file = RareSquare
                            break       
                        case "very rare":
                            file = VeryRareSquare
                            break
                        case "ultra rare":
                            file = UltraRareSquare
                            break 
                        case "event":
                            file = EventSquare
                            break
                    }
                    break

                case "add-on":
                    switch(rarity.toLowerCase()) {
                        case "common":
                            file = CommonSquare
                            break
                        case "uncommon":
                            file = UncommonSquare
                            break
                        case "rare":
                            file = RareSquare
                            break       
                        case "very rare":
                            file = VeryRareSquare
                            break
                        case "ultra rare":
                            file = UltraRareSquare
                            break   
                        case "event":
                            file = EventSquare
                            break                        
                    }

                    break 
    
                case "offering":
                    switch(rarity.toLowerCase()) {
                        case "common":
                            file = CommonOffering
                            break                    
                        case "uncommon":
                            file = UncommonOffering
                            break;
                        case "rare":
                            file = RareOffering
                            break;          
                        case "very rare":
                            file = VeryRareOffering
                            break;  
                        case "ultra rare":
                            file = UltraRareOffering
                            break    
                        case "event":
                            file = EventOffering
                            break                                              
                    }
                    break                                             
            }
        }
        return file
    }

    useEffect(() => {
        if(rarities) {
            setRarityIndex(0)
            setFilename(getFilename(0))
        } else if(type) {
            let type__lower = type.toLowerCase()

            switch(type__lower) {
                case "perk":
                    setFilename(UncommonPerk)
                    break
                case "item":
                    setFilename(CommonSquare)
                    break
                case "power":
                    setFilename(CommonSquare)
                    break
                case "add-on":
                    setFilename(CommonSquare)
                    break
                case "offering":
                    setFilename(CommonOffering)
                    break
            }
        }
    }, [rarities, type])


    return(
        <div 
        className={`Icon Icon--${
            size==SIZES[0]
            ? "sm"
            : "md"
            }`
        }
        onClick={toggleRarities}>
            {filename && <img 
                className="Icon-bg" 
                src={filename}
            />}
            {(type && type.toLowerCase() == "perk")
                ? <img className="Icon-image" src={src} title="Click to Change Tier" />
                : <img className="Icon-image" src={src} />
            }
            {false && <div className="Icon-info scrollbar">
                <div className={`Icon-info-header Icon--${
                    rarity
                    // CSS classes don't contain space characters
                    ? rarity.toLowerCase().replace(" ", "-")
                    : "common"}`}>
                    <div className="Icon-info-tier">
                        {tier? `${name} ${tier}`:`${name}`}
                    </div>
                    {rarity
                    ? type
                        ?<div className="Icon-info-owner">
                            <span>{rarity} {type} {(reference != type) && reference}</span>
                        </div>
                        :<div className="Icon-info-rarity">
                            <span>{rarity} {reference}</span>
                        </div>
                    :<div className="Icon-info-owner">
                        <span>{reference}</span>
                    </div>}
                </div>
                <div className="Icon-info-description">
                    {description}
                </div>
                {quote && <div className="Icon-info-quote">
                    {quote}
                </div>}
            </div>}
        </div>
    )
}