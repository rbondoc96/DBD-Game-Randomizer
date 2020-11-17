import React, {useState} from "react"

function Button({
    href,
    type="button",
    children,
}) {

    return(
        <div className="Button">
            {href
            ? <a href={href}>
                <button type={type}>
                    {children}
                </button>
            </a>
            : <button type={type}>
                {children}
            </button>}
        </div>
    )
}

export default function GameForm({

}) {
    const [form, setForm] = useState({
        gameType: null,
        numPlayers: null,
    })

    const onChange = event => {
        var self = event.currentTarget
        var name = self.getAttribute("name")
        console.log(self)
        console.log(form)
        setForm({
            ...form,
            [name]: self.value
        })
    }

    return(
        <>
            <form method="GET" action="/api/game">
                <label htmlFor="game-type">Game Type</label>
                <select id="game-type" name="gameType" onChange={onChange}>
                    <option value="killer">Killer (1 player)</option>
                    <option value="survivor">Survivor (1-4 players)</option>
                    <option value="custom">Custom Game (2-5 players)</option>
                </select>
                <label htmlFor="num-players">Number of Players</label>
                <select id="num-players" name="numPlayers" onChange={onChange}>
                    <option value="1">1</option>
                    {form.gameType == "survivor" &&
                    <>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                    </>}
                    {form.gameType == "custom" &&
                    <>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                    </>
                    }
                </select>
                <Button type="submit" children="Submit" />
            </form>
        </>
    )
}