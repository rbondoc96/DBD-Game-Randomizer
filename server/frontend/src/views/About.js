import React from "react"

import InlineLink from "../components/page/InlineLink"
import Player from "../components/player/Player"

import Page, {
    PageHeader, 
    PageFooter,
    PageSubheader, 
    PageText
} from "../components/page/Page"

const ExampleSurvivor = () => {
    let character = {
        name: "Meg Thomas",
        image: "/assets/characters/Survivors/Meg_Thomas.png"
    }
    let item = {
        rarities: ["Ultra Rare"],
        overlay: "/assets/overlays/items/Rainbow_Map.png"
    }
    let item_addons = [
        {
            rarities: ["Rare"],
            overlay: "/assets/overlays/addons/items/Black_Silk_Cord.png"
        }, {
            rarities: ["Very Rare"],
            overlay: "/assets/overlays/addons/items/Crystal_Bead.png"
        }
    ]
    let offering = {
        name: "Tarnished Coin",
        rarities: ["Uncommon"],
        overlay: "/assets/overlays/offerings/survivor/Tarnished_Coin.png"
    }
    let perks = [
        {
            name: "Bond",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/survivor/Bond.png"
        },
        {
            name: "Lightweight",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/survivor/Lightweight.png"
        },
        {
            name: "Lucky Break",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/survivor/Lucky_Break.png"
        },
        {
            name: "Urban Evasion",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/survivor/Urban_Evastion.png"
        }
    ]
    let role = "Survivor"

    let player = {
        name: "Potato",
        role: role,
        player_id: "ABCD1234",
        character: character,
        item: item,
        item_addons: item_addons,
        power_addons: [],
        perks: perks,
        offering: offering
    }

    return(<Player 
        role={role}
        data={player}
    />)
}

const ExampleKiller = () => {
    let character = {
        name: "The Hag",
        image: "/assets/characters/Killers/The_Hag.png"
    }
    let power = {
        rarities: ["Ultra Rare"],
        primary_overlay: "/assets/overlays/powers/Blackened_Catalyst-primary.png"
    }
    let power_addons = [
        {
            rarities: ["Rare"],
            overlay: "/assets/overlays/addons/items/Black_Silk_Cord.png"
        }, {
            rarities: ["Very Rare"],
            overlay: "/assets/overlays/addons/items/Crystal_Bead.png"
        }
    ]
    let offering = {
        name: "Tarnished Coin",
        rarities: ["Uncommon"],
        overlay: "/assets/overlays/offerings/survivor/Tarnished_Coin.png"
    }
    let perks = [
        {
            name: "A Nurse's Calling",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/killer/A_Nurses_Calling.png"
        },
        {
            name: "Agitation",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/killer/Agitation.png"
        },
        {
            name: "Bamboozle",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/survivor/Bamboozle.png"
        },
        {
            name: "Barbecue & Chili",
            rarities: ["Uncommon", "Rare", "Very Rare"],
            overlay: "/assets/overlays/perks/killer/Barbecue__Chili.png"
        }
    ]
    let role = "Killer"

    let player = {
        name: "Sweaty",
        role: role,
        player_id: "ZYXW9876",
        character: character,
        power: power,
        item_addons: [],
        power_addons: power_addons,
        perks: perks,
        offering: offering
    }

    return(<Player 
        role={role}
        data={player}
    />)
}

export default function About() {

    return(
        <Page classes={"scrollbar overflow-y-auto"}>
            <PageHeader>About This Randomizer</PageHeader>
            <PageText classes="About-text">
                <InlineLink href={"https://deadbydaylight.com"} children={"Dead by Daylight"} /> is an asymmetrical action-horror game developed by Behaviour Interactive. In every Trial, one player takes the role of a Killer while four others play as Survivors.
            </PageText>
            <PageText classes="About-text">
                This randomizer generates combinations of 4 Perks, 1 Offering, and an Item and 2 Add-ons for Survivors, or a Power and 2 Add-ons for Killers.
            </PageText>
            <div className="About-examples">
                <ExampleSurvivor />    
                <ExampleKiller />
            </div>
            <PageText classes="About-text">
                Perks have 3 tiers, its effects improving with every tier. By default, Tier 1 (Uncommon) is displayed. <strong>Click on the Perk's icon to toggle between the 3 tiers.</strong>
            </PageText>

            <PageSubheader>Randomize with Friends</PageSubheader>
            <PageText classes="About-text">
                Playing with friends? Randomize your builds together in real-time session rooms and know what your friends are bringing into the next Trial. Sessions will also try to guess which player the Obsession is and which Realm the Trial will be in.
            </PageText>

            <PageText classes="About-text">
                From the Sessions page, create a new session or join an existing one, if you have the session ID handy.
            </PageText>

            <PageSubheader tag="h3">Session Hosts</PageSubheader>
            <PageText classes="About-text">
                Whenever a player creates a new session, that player will be the Session's Host. In Custom Game sessions, the Host is always the Killer. 
            </PageText>

            <PageText classes="About-text">
                The Host can hand over their role to another player in the session if they choose. If the Host leaves the session, another Player will become the Host. If there are no Players left in a session, the session is destroyed.
            </PageText>

            <PageSubheader tag="h3">Real-Time Updates</PageSubheader>
            <PageText classes="About-text">
                Whenever a Player randomizes their build, all Players in the session will see the changes. The session's Obsession and Realm may also change.
            </PageText>

            <PageSubheader>Contributing</PageSubheader>
            <PageText classes="About-text">
                This project is open-source and can be found on <InlineLink href={"https://github.com"} children={"Github."} />
            </PageText>
        </Page>
    )
}