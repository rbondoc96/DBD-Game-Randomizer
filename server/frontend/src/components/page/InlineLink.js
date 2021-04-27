import React from "react"

export default function InlineLink({
    href,
    blank=true,
    children,
}) {
    
    return(<span className="InlineLink"><a href={href} target={blank? "_blank" : ""}>
        {children}
    </a></span>)
}