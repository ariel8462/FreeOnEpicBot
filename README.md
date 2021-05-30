# FreeOnEpicBot
A telegram bot that will notify when games become free on all platforms such as Steam, Epic Games etc

## Commands:
- `/subscribe` - suscribe for notifications about new games
- `/unsubscribe` - unsuscribe from notifications about new games
- `/freegame` - show the current free game
- `/help` - show basic bot info`

## Setting up: 
- Clone the repo
- Go to the directory and `pip install -r requirements.txt`
- Change the sample_config to config.py and insert your bot token
- Either host locally or deploy to heroku
- For hosting locally run: `python FreeOnEpicBot.py` (inside the file's directory)
- If you deploy to heroku remove the `.gitignore` and deploy with heroku cli
- Note: on Linux it's "python3" and "pip3" instead of "python" and "pip"
