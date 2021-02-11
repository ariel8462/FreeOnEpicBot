import feedparser
import telegram
from telegram.ext import Updater, CommandHandler
import logging
import threading

"""
A bot token for the bot, and your user id (you will be the only one with access to the bot)
"""
token = "BOT_TOKEN_HERE"
user_id = 'USER_ID_HERE'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

free_game_list = []


def send_message(chat_id, text, token=token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=user_id, text=text)


def get_links(url="https://www.indiegamebundles.com/category/free/rss"):
    d = feedparser.parse(url)
    free_description = d.entries[0].title
    free_link = d.entries[0].link
    threading.Timer(600.0, get_links).start()
    if free_link not in free_game_list:
        free_game_list.append(free_link)
        if len(free_game_list) == 1:
            pass
        else:
            send_message(chat_id=user_id, text=f"""{free_description}
{free_link}""")
    return f""" {free_description}
{free_link}"""


free_right_now = get_links()


def free_game(update, context):
    bot = context.bot
    user = update.effective_user
    if not update.message.chat.type == "private":
        return
    if update.effective_user.id != user_id:
        return
    bot.send_message(chat_id=user_id, text=free_right_now)


def help_command(update, context):
    bot = context.bot
    user = update.effective_user
    if not update.message.chat.type == "private":
        return
    if update.effective_user.id != user_id:
        return
    bot.send_message(chat_id=user_id, text=
    """Hi there, I am a bot that shows you the current free games on all the major game platforms out there
You will get automatically notified when new games become available for free
If you want to see the current free game please use the following command: /freegame
""")


def main():
    updater = Updater(token=token)
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher
    logger.info('The bot has started')
    dp.add_handler(CommandHandler('freegame', free_game))
    dp.add_handler(CommandHandler("help", help_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
