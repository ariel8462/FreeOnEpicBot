import feedparser
import telegram
from telegram.ext import Updater, CommandHandler, JobQueue
import logging
from config import Config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

free_game_list = []


class FreeOnEpic:
    """
    A class that represents the bot and contains all of it's methods
    """
    bot_token = Config.BOT_TOKEN
    user_id = Config.USER_ID

    def send_message(text):
        bot = telegram.Bot(token=FreeOnEpic.bot_token)
        bot.sendMessage(chat_id=FreeOnEpic.user_id, text=text)

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
                    FreeOnEpic.send_message(text=f"""{free_description}
            {free_link}""")
            return f""" {free_description}
            {free_link}"""
        except Exception as e:
            FreeOnEpic.send_message(text=f"The site is currently down or unreachable:\n{e}")

    free_right_now = get_links("")

    def free_game(update, context):
        """
        Sends the current free game via telegram
        """
        bot = context.bot
        if not update.message.chat.type == "private":
            return
        if update.effective_user.id != FreeOnEpic.user_id:
            return
        bot.send_message(chat_id=FreeOnEpic.user_id, text=FreeOnEpic.free_right_now)

    def help_command(update, context):
        """
        Sends basic information about the bot and explains it's use in short via telegram
        """
        bot = context.bot
        if not update.message.chat.type == "private":
            return
        if update.effective_user.id != FreeOnEpic.user_id:
            return
        bot.send_message(chat_id=FreeOnEpic.user_id, text=FreeOnEpic.help_message)

    help_message = """Hi there, I am a bot that shows the current free games on all the major game platforms out there.
You will get automatically notified when new games become free to collect.
If you would like to see the current free game please use the following command:  /freegame
    """


def main():
    updater = Updater(token=FreeOnEpic.bot_token, use_context=True)
    dp = updater.dispatcher
    job_queue = JobQueue()
    job_queue.set_dispatcher(dp)
    job_queue.run_repeating(callback=FreeOnEpic.get_links, interval=600)
    logger.info('The bot has started')
    dp.add_handler(CommandHandler('freegame', FreeOnEpic.free_game))
    dp.add_handler(CommandHandler("help", FreeOnEpic.help_command))
    job_queue.start()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
