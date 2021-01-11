<h1 align="center">Dead by Daylight Game Randomizer</h1>

<p align="center"><b>********** Currently in development **********</b></p>

<a href="https://deadbydaylight.com/en">Dead by Daylight</a> is a popular asymmetrical, online multiplayer horror game where 1 player takes the role of a Killer and 4 others play as Survivors. This application allows users to create and join online game sessions where they can randomize their player loadouts for everyone in the session to see in real-time.

### Features
- A full database that is regularly updated upon each new addition to the game
- Real-time sessions with up to 5 other players in Custom games 
- Lists the total effects that a randomized build has on the player and on the game session

## Project Status
- Status: Development

## Roadmap
- Project Start: November 2020

## Technologies

### Front-End
- SCSS
- JavaScript
    - Libraries & Frameworks: React JS
- Webpack
### Back-End
- Python
    - Libraries & Frameworks: Django, Django REST, Django Channels
- PostgreSQL
- Docker
    - Runs a Redis image

### Installing Packages
To install the Python and JavaScript packages, run the following commands from the root project directory:

```bash
/ > pipenv shell        # Initialize virtual environment
/ > pipenv install      # Install Python packages from the Pipfile
/ > cd server/frontend  # Navigate to frontend app
/server/frontend > npm install      # Install JavaScript packages
```

### Building Front-End Files (Development)
```bash
/server/frontend > npm start       # Start WebPack build
```

### Starting Development Server
```bash
/server/ > python manage.py runserver   # Start Django dev server and ASGI
```

## Sources
- Game Icon Pack
    - <a href="https://www.reddit.com/r/PerkByDaylight/comments/jsljrb/toon_pack_a_binding_of_kin_update/">Toon Pack</a> by Reddit user u/Shirbler
        - Current Updated Release: A Binding of Kin
- Character Portraits, Template Images, and Descriptions
    - <a href="https://deadbydaylight.gamepedia.com/Dead_by_Daylight_Wiki">Dead by Daylight Gamepedia</a>

## Future Features/Ideas
- Registered User Accounts
    - Track their own perks per in-game character to randomize builds from
