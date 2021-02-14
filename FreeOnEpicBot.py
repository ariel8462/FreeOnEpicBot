import feedparser
import telegram
from telegram.ext import Updater, CommandHandler
import logging
import threading

"""
A bot token for the bot, and a userID for the control over the bot
"""
with open("BOT_TOKEN.txt") as f:
    token = f.read().strip()
with open("USER_ID.txt") as f:
    user_id = f.read().strip()
    user_id = int(user_id)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

free_game_list = []


def send_message(chat_id, text, token=token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=user_id, text=text)


def get_links(url="https://www.indiegamebundles.com/category/free/rss"):
    """
    Parses new games from the rss feed and formats them into a compact-looking message

    Args:
        url (str): rss feed of a specific site, in this case the feed of a "Game News" site
    Returns:
        a ready to go message that contains the current's free game link + description
    """
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
    """
    Sends the current free game via telegram
    """
    bot = context.bot
    if not update.message.chat.type == "private":
        return
    if update.effective_user.id != user_id:
        return
    bot.send_message(chat_id=user_id, text=free_right_now)


def help_command(update, context):
    """
    Sends basic information about the bot and explains it's use in short via telegram
    """
    bot = context.bot
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
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher
    logger.info('The bot has started')
    dp.add_handler(CommandHandler('freegame', free_game))
    dp.add_handler(CommandHandler("help", help_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
