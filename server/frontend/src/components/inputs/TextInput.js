import React from "react"

export default function TextInput({
    label,
    id,
    name,
    value,
    placeholder,
    onChange,
    maxLength,
}) {

    return(
        <div className="TextInput">
            <label htmlFor={id}>{label}</label>
            <input 
                type="text" 
                id={id}
                name={name} 
                onChange={onChange}
                defaultValue={value}  
                placeholder={placeholder}
                maxLength={maxLength}
            />
        </div>
    )
}