# Project Started: Monday, November 9, 2020

## Technologies
- Development
    * Frontend
        - JavaScript -- React JS
        - Webpack, Webpack CLI
    * Backend
        - Python -- Django
        - Django REST
- Production
    * Backend
        - NGINX -- serve static files and images
- Database
    - PostgreSQL


## Web Application Features
1. 3 Game Modes
    a. Killer
        - 1 player
    b. Survivor
        - 1 to 4 players
    c. Custom Game
        - 2 to 5 players
2. Ability to "anchor" values from randomizing
3. Decent graphical interface, using the Toon Pack
4. Character Portraits
5. Map Portraits or ??? if the map is unknown
6. Summary of Effects for each player
7. Obsession: _____ or ??? if the obsession is unknown

## Docker Workflow
- Build Docker image after changes
- If changes need to happen, make changes in local repo
- After changes happen, build Docker image again


### Future Features/Ideas
- Users can create an account and track the perks they have on each character
    - This lets the randomizer randomize perks that they actually have in game.
        - The caveat is, the user themselves will need to add perks as they acquire them
- For Survivor and Custom Games, users can join server rooms of 2 up to (4 if Survivor or 5 if Custom Game)
- For Custom Games:
    - Killer perks and effects are hidden from survivors
    - Survivor perks and effects are hidden from killers
    - There is a toggle button for each
