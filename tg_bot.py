import logging
import sys
from functools import partial
from time import sleep

import telegram
from environs import Env
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from modules import LogsHandler, detect_intent_texts


LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте!")


def reply_to_message(update: Update, context: CallbackContext,
                     project_id: str) -> None:
    session_id = f'tg-{update.effective_user.id}'

    try:
        answer = detect_intent_texts(
            project_id, session_id, update.message.text, LANGUAGE_CODE
        )
        update.message.reply_text(answer.fulfillment_text)
    except NetworkError as netword_error:
        logger.warning(f'Network error: {netword_error}\n')
        sleep(20)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")
    user_id = env.str('USER_ID')
    project_id = env.str('PROJECT_ID')
    bot = telegram.Bot(token=tg_token)
    logging.basicConfig(
        filename='tg_app.log',
        filemode='w',
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.addHandler(LogsHandler(bot, user_id))
    logger.info('Бот запущен')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text,
                           partial(reply_to_message, project_id=project_id)))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
