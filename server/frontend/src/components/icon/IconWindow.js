import React, {useState, useContext} from "react"

import {IconContext} from "../../context/IconContext"

export default function IconWindow({
    src,
    type,
    icon_type,
    name,
    tier,
    description,
    quote,
}) {
    const [icon, setIcon] = useContext(IconContext)
    const [isHidden, setIsHidden] = useState(true)

    const onClick = event => {
        console.log("Icon", icon)
        setIsHidden(!isHidden)
    }
    let rarity__lower = (icon && icon.rarity)? icon.rarity.toLowerCase().replace(" ", "-") : ""

    return(
        <>
        {icon && <div className={isHidden? "IconWindow--hidden" : "IconWindow"}>
            <div className={`IconWindow-header ${
                icon.rarity? rarity__lower : "common"
            }`}>
                <div className="IconWindow-header-toggle">
                    <button onClick={onClick}>
                        V
                    </button>
                </div>
                <div className="IconWindow-header-content IconWindow-content">
                    <div className="IconWindow-header-name">
                        <h1>
                            <span>{icon.name}</span>
                            {icon.tier && <span>
                                {icon.tier}
                            </span>}
                        </h1>
                    </div>
                    <div className="IconWindow-header-class">
                        {icon.rarity && <span className="IconWindow-header-class-rarity">
                            {icon.rarity}
                        </span>}
                        {icon.reference && <span className="IconWindow-header-class-reference">
                            {icon.reference}
                        </span>}
                        {icon.type && <span className="IconWindow-header-class-owner">
                            {icon.type}
                        </span>}
                    </div>
                </div>
            </div>
            <div className="IconWindow-main IconWindow-content scrollbar">
                <div className="IconWindow-main-description">
                    <pre className="IconWindow-main-description-text">
                        {icon.description}
                    </pre>
                    {icon.quote && <em className="IconWindow-main-description-quote">
                        {icon.quote}
                    </em>}
                </div>
                <div className="IconWindow-main-image">
                    <img src={icon.src} />
                    {icon.src2 && <div className="IconWindow-main-image-extras">
                        <img src={icon.src2} />
                        {icon.src3 && <img src={icon.src3} />}
                    </div>}
                </div>
                <div className="IconWindow-main-separator"></div>
                <div className="IconWindow-main-stats">
                    <h3 className="IconWindow-main-stats-header">

                    </h3>
                    <div className="IconWindow-main-stats-content">

                    </div>
                </div>
            </div>
        </div>}
        </>
    )
}