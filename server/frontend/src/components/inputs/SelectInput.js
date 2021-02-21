import React from "react"

export default function SelectInput({
    label,
    id,
    name,
    value,
    onChange,
    children,
    ref,
}) {

    return(
        <div className="SelectInput">
            <label htmlFor={id}>{label}</label>
            <select 
                id={id}
                name={name} 
                value={value}  
                onChange={onChange}
                children={children}
                ref={ref}
            />
        </div>
    )
}