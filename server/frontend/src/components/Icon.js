import React, {useRef} from "react";

export default function Icon({
    name,
    src,
}) {
    const imgRef = useRef(null)
    return(
        <div className="icon-container">
            <div>
                <img className="icon" src={src} />
            </div>
            <p className="icon-name">
                {name}
            </p>
        </div>
    )
}