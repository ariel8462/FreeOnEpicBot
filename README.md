# FreeOnEpicBot
A telegram bot that will notify when games become free on all platforms such as Steam, Epic Games etc

## Commands:
- `/freegame` - show the current free game
- `/help` - show basic bot info

No other commands, the bot notifies when new games become free automatically

## Setting up: 
- Clone the repo
- Go to do directory and `pip install -r requirements.txt` note: it's pip3 on linux
- Remove the '_example' from `BOT_TOKEN_example.txt` and `USER_ID_example.txt`
- Put your desired bot ID in `BOT_TOKEN.txt` and your user ID in `USER_ID.txt`
- Either host locally or deploy to heroku
- For hosting locally run: `python FreeOnEpicBot.py` note: it's python3 on linux


## Marks:
- The code can be better, just got busy and no time for refactoring/improvements, will be happy for feedback!
