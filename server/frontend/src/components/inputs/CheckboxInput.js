import React from "react"

export default function CheckboxInput({
    id,
    name,
    label,
    onChange,
}) {
    
    return(
        <div className="CheckboxInput">
            <label htmlFor={id}>
                <input 
                    type="checkbox"
                    id={id}
                    name={name}
                    label={label}
                    onChange={onChange}
                />
                {label}
            </label>
        </div>
    )
}