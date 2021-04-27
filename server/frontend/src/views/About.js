import React from "react"

import InlineLink from "../components/page/InlineLink"

import Page, {
    PageHeader, 
    PageFooter,
    PageSubheader, 
    PageText
} from "../components/page/Page"

export default function About() {

    return(
        <Page>
            <PageHeader>About This Randomizer</PageHeader>
            <PageSubheader>What is Dead by Daylight?</PageSubheader>
            <PageText classes="About-text">Some text</PageText>

            <PageSubheader>How to Use This Randomizer</PageSubheader>
            <PageText classes="About-text">Some text</PageText>

            <PageSubheader>Contributing</PageSubheader>
            <PageText classes="About-text">Some text</PageText>

            <PageFooter>
                <PageText classes="About-footer-text">The footer text <InlineLink href={"https://github.com"} children={"Github"} /> leads to the site</PageText>
            </PageFooter>
        </Page>
    )
}