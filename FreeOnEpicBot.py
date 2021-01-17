import feedparser
import telegram
from telegram.ext import Updater, CommandHandler
import logging
import threading

token = "1447754233:AAHxpRbmZH2IbrVFAo8sShCGnQX3vpsw9fo"
user_id = 1170714920

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


def main():
    updater = Updater(token=token, use_context=True)
    dp = updater.dispatcher
    logger.info('The bot has started')
    dp.add_handler(CommandHandler('freegame', free_game))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
