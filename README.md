# FreeOnEpicBot
A telegram bot that will notify when games become free on all platforms such as Steam, Epic Games etc

## Commands:
- `/freegame` - show the current free game
- `/help` - show basic bot info

No other commands, the bot notifies when new games become free automatically

## Setting up: 
- Clone the repo
- Go to the directory and `pip install -r requirements.txt`
- Change the sample_config to config.py and insert your user id & bot token
- Either host locally or deploy to heroku
- For hosting locally run: `python FreeOnEpicBot.py` (inside the file's directory)
- If you deploy to heroku remove the `.gitignore` and deploy with heroku cli
- Note: on Linux it's "python3" and "pip3" instead of "python" and "pip"
