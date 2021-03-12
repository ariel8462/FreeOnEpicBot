import feedparser
import telegram
from telegram.ext import Updater, CommandHandler, JobQueue
import logging

help_message = """Hi there, I am a bot that shows the current free games on all the major game platforms out there.
You will get automatically notified when new games become free to collect.
If you would like to see the current free game please use the following command:  /freegame
"""

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


def send_message(text):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=user_id, text=text)


def get_links(context):
    """
    Parses new games from the rss feed and formats them into a compact-looking message

    Returns:
        a ready to go message that contains the current's free game link + description
    """
    url = "https://www.indiegamebundles.com/category/free/rss"
    try:
        d = feedparser.parse(url)
        free_description = d.entries[0].title
        free_link = d.entries[0].link
        if free_link not in free_game_list:
            free_game_list.append(free_link)
            if len(free_game_list) == 1:
                pass
            else:
                send_message(text=f"""{free_description}
        {free_link}""")
        return f""" {free_description}
        {free_link}"""
    except Exception as e:
        send_message(text=f"The site is currently down or unreachable:\n{e}")


free_right_now = get_links("")


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
    bot.send_message(chat_id=user_id, text=help_message)


def main():
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher
    job_queue = JobQueue()
    job_queue.set_dispatcher(dp)
    job_queue.run_repeating(callback=get_links, interval=600)
    logger.info('The bot has started')
    dp.add_handler(CommandHandler('freegame', free_game))
    dp.add_handler(CommandHandler("help", help_command))
    job_queue.start()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
