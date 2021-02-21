import React, {useRef, useContext} from "react";

import {IconContext} from "../../context/IconContext"

const SIZES = ["small", "medium"]

export default function Icon({
    src,
    src2,
    src3,
    type,
    reference,
    name,
    tier,
    rarity,
    description,
    quote,
    effects,
    size=SIZES[1]
}) {
    // Renaming to mainIcon to differentiate with the current instance
    const [mainIcon, setMainIcon] = useContext(IconContext)

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

    var iconTypeInfo

    if(type) {
        iconTypeInfo = <span>{rarity} {type} {reference}</span>
    } else if(reference == "add-on") {
        iconTypeInfo = <span>{rarity} {"An Item Type"} {reference}</span>
    } else {
        iconTypeInfo = <span>{rarity} {reference}</span>
    }


    return(
        <div 
        className={`Icon Icon--${
            size==SIZES[0]
            ? "sm"
            : "md"
            }`
        }
        onClick={setAsMainIcon}>
            <img className="Icon-image" src={src} />
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