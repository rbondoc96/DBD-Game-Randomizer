import React from "react"

export default function Admin({

}) {
/*
    A one page, dynamic form

    /api/admin/ -- restricted to Me
    
    Allows me to switch between all models via a Select Field
    Another Select Field populates with all Model Objects

    A Form for the Model will dynamically render
    (Have server send HTML in JSON response?)
    - Blank if Add New Button is clicked
    - With Entry Info if the modelObject is clicked
       - Options to Edit or Delete the Entry
*/
    <>
        <div className="admin">
            <select id="model" name="model">

            </select>
            <select id="model-objects" name="modelObjects">

            </select>


            <button>Add New</button>
            <button>Edit</button>
            <button>Delete</button>
        </div>
    </>
}