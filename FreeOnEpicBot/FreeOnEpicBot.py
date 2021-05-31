import feedparser
import telegram
from telegram.ext import Updater, CommandHandler, JobQueue
import config
import logging
import json
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
free_game_list = []
bot_token = config.BOT_TOKEN

if os.path.exists('data.json'):
    with open('data.json', 'r') as chat_data:
        chat_db = json.load(chat_data)
else:
    chat_db = {}


def send_message(text):
    bot = telegram.Bot(token=bot_token)
    for id in chat_db.values():
        try:
            bot.sendMessage(chat_id=id, text=text)
        #In case the group/user is non-existent
        except Exception as e:
            logging.warning(f"The following chat ID doesn't exist - {e}")
            for key, value in chat_db.items():
                if value == id:
                    del chat_db[key]
                    break
            with open('data.json', 'w') as chat_data:
                json.dump(chat_db, chat_data)


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
                send_message(text=f"{free_description}\n{free_link}")
        return f"{free_description}\n{free_link}"
    except Exception as e:
        send_message(text=f"The site is currently down or unreachable:\n{e}")


free_right_now = get_links('')


def free_game(update, context):
    """
    Sends the current free game via telegram
    """
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text=free_right_now)


def help_command(update, context):
    """
    Sends basic information about the bot and explains it's use in short via telegram
    """
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text=config.HELP_MESSAGE)


def subscribe(update, context):
    """
    Adds the chat ID to the json file for future reference
    """
    bot = context.bot
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.username
    for id in chat_db.values():
        if chat_id == id:
            bot.send_message(chat_id=update.effective_chat.id, text="You are already subscribed!")
            return
    else:
        chat_db.update({chat_name: chat_id})
        with open('data.json', 'w') as chat_data:
            json.dump(chat_db, chat_data)
        bot.send_message(chat_id=update.effective_chat.id, text="You have succefully subscribed!")


def unsubscribe(update, context):
    """
    Removes the chat ID from the json file
    """
    bot = context.bot
    chat_id = update.effective_chat.id
    for id in chat_db.values():
        if chat_id == id:
            for key, value in chat_db.items():
                if value == chat_id:
                    del chat_db[key]
                    bot.send_message(chat_id=update.effective_chat.id, text="You have succefully unsubscribed!")
                    with open('data.json', 'w') as chat_data:
                        json.dump(chat_db, chat_data)
                    return
    else:
        bot.send_message(chat_id=update.effective_chat.id, text="You are not even subscribed!")
        return


def main():
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    job_queue = JobQueue()
    job_queue.set_dispatcher(dp)
    job_queue.run_repeating(callback=get_links, interval=600)
    logger.info('The bot has started')
    dp.add_handler(CommandHandler('freegame', free_game))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    job_queue.start()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
