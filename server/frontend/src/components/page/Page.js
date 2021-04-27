import React from "react"

export default function Page({
    classes="",
    children,
}) {

    let classNames = `Page ${classes}`

    return(
        <div className={classNames}>
            {children}
        </div>
    )
}

export function PageHeader({
    tag="h1",
    classes="",
    children,
}) {
    let htmlTag = getTag(tag, children)
    let classNames = `PageHeader ${classes}`

    return(
        <div className={classNames}>
            {htmlTag}
        </div>
    )
}

export function PageFooter({
    classes="",
    children,
}) {

    let classNames = `PageFooter ${classes}`

    return(
        <footer className={classNames}>
            {children}
        </footer>
    )
}

export function PageSubheader({
    tag="h2",
    classes="",
    children,
}) {
    let htmlTag = getTag(tag, children)
    let classNames = `PageSubheader ${classes}`

    return(
        <div className={classNames}>
            {htmlTag}
        </div>
    )
}

export function PageText({
    tag="div",
    classes="",
    children,
}) {
    let htmlTag = getTag(tag, children)
    let classNames = `PageText ${classes}`

    return(
        <div className={classNames}>
            {htmlTag}
        </div>
    )
}

function getTag(tag, children) {
    switch(tag.toLowerCase()) {
        case "h1":
            return(<h1>{children}</h1>)

        case "h2":
            return(<h2>{children}</h2>)

        case "h3":
            return(<h3>{children}</h3>)
        
        case "h4":
            return(<h4>{children}</h4>)
        
        case "h5":
            return(<h5>{children}</h5>)       

        case "div":
            return(<div>{children}</div>)       

        case "p":
            return(<p>{children}</p>)       

        default:
            return(<div>{children}</div>)
    }
}