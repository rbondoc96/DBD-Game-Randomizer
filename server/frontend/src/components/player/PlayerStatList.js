import React, {useRef} from "react"

export default function PlayerStatList({
    header,
    titles,
    bulletList,
    onClick,
    activeStatList=null,
}) {
    const self = useRef(null)

    return(
        <div className="PlayerStatList" onClick={onClick} ref={self}>
            <div className={`PlayerStatList-header${
                    (activeStatList==self.current) && (self.current!=null)
                    ? "--active"
                    : ""}`}>
                <div className="PlayerStatList-header-line"></div>
                <span className="PlayerStatList-header-text">{header}</span>
                <div className="PlayerStatList-header-line"></div>
            </div>
            <div className={`PlayerStatList-content scrollbar ${
                (activeStatList==self.current) && (self.current!=null)
                ? "d-block" 
                : "d-none" }`}>
                Hi
                <br />
                <br />
                <br />
                Hi
                <br />
                Hi
                <br />
                <br />
                <br />
                Hi
                <br />
                Hi
                <br />
                <br />
                <br />
                Hi
                <br />
            </div>  
        </div>
    )
}