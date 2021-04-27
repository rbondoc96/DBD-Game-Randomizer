import React, {useState, useRef, useContext, useEffect} from "react"

import {SelfContext} from "../context/SelfContext"

import Page, {
    PageHeader,
    PageSubheader,  
    PageText
} from "../components/page/Page"

export default function Settings() {

    const self = useContext(SelfContext)[0];

    useEffect(() => {

    }, [self])

    let name = (self && self.name) ? self.name : "Anonymous"
    let id = (self && self.player_id) ? self.player_id : "********"  

    return(
        <Page>
            <PageHeader classes="Settings-header">Player Settings</PageHeader>
            <PageSubheader tag="div" classes="Settings-info">
                {name}<span>#{id}</span>
            </PageSubheader>
            <PageText>
                <SettingsEditableTextField 
                    label="Player Name"
                    initialValue={name}
                    fieldName="name"
                    buttonText="edit name"
                />
                <SettingsTextField
                    label="Player ID"
                    value={id}
                />
            </PageText>
        </Page>        
    )
}

/*
A component that where the user can edit a text-based field. 
The component will call the Player api and changed the corresponding field.

# Parameters    
label           - Label for the field
initialValue    - Initial value before changes
fieldName       - Field name in the api
buttonText      - Button Text to toggle edit
*/
function SettingsEditableTextField({
    label,
    initialValue,
    fieldName,    
    buttonText,
 }) {
    
    const setSelf = useContext(SelfContext)[1];
    const [editable, setEditable] = useState(false)
    const [value, setValue] = useState(initialValue)
    const valueRef = useRef(null)

    /* Allows state to change after Player data is received from Player API and passed to this component as a prop */
    useEffect(() => {
        setValue(initialValue)
    }, [initialValue])
    
    const handleEditClick = event => {
        if(!editable) {
            /* Wrapping calls in setTimeout( ,0) makes focus() work */
            setTimeout(() => {
               valueRef.current.focus()
               setCursorAtEndOfContentEditable(valueRef.current)
            }, 0)
         } else {
            /* Value is editable, user is confirming changes */
            
            /* Call Player API */
            let params = new URLSearchParams({
                "action": "rename",
                "name": valueRef.current.textContent
            })
            
            fetch("/api/player/?" + params)
            .then(res => res.json())
            .then(json => {
                console.log("Renamed", json)
                setSelf(json.player)
                setValue(json.player.name)
            })
         }
         setEditable(!editable)      
         valueRef.current.classList.toggle("SettingsEditableTextField-value--editable")
     }
     
     const handleRevertClick = event => {
        if(valueRef.current.classList.contains("SettingsEditableTextField-value--editable"))
           valueRef.current.classList.remove("SettingsEditableTextField-value--editable")        
              
        setEditable(false)
        /* Restore to current value */
        valueRef.current.textContent = value
     }
    
    return(
       <div className="SettingsEditableTextField">
            <span className="SettingsEditableTextField-label">{label}:</span>

            <span 
                className="SettingsEditableTextField-value" 
                ref={valueRef} 
                contentEditable={editable}
            >{initialValue}</span>

            <button className="SettingsEditableTextField-button" onClick={handleEditClick}>
                {editable? "confirm changes?" : buttonText}
            </button>
            
            {editable && <button className="SettingsEditableTextField-button" onClick={handleRevertClick}>
                revert changes
            </button>}              
       </div>
    )
}

 /* Solution for function from: https://stackoverflow.com/a/3866442 */
function setCursorAtEndOfContentEditable(element) {
    var range,selection;
    if(document.createRange)    //Firefox, Chrome, Opera, Safari, IE 9+
    {
        range = document.createRange();
        range.selectNodeContents(element);
        range.collapse(false);
        selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }
    else if(document.selection)
    { 
        range = document.body.createTextRange();
        range.moveToElementText(element);
        range.collapse(false);     
        range.select();    
    }
}

/* 
Basically SettingsEditableTextField, but not editable. Same styles
*/
function SettingsTextField({
    label,
    value,
}) {
    
    return(
       <div className="SettingsTextField">
            <span className="SettingsTextField-label">{label}:</span>

            <span className="SettingsTextField-value">{value}</span>           
       </div>
    )
}