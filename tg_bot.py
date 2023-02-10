import logging
from functools import partial
from time import sleep

from environs import Env
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from modules import detect_intent_texts


LANGUAGE_CODE = 'ru-RU'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Здравствуйте!")


def reply_to_message(update: Update, context: CallbackContext,
                     project_id) -> None:
    session_id = f'tg-{update.effective_user.id}'

    try:
        answer = detect_intent_texts(
            project_id, session_id, update.message.text, LANGUAGE_CODE
        )
        update.message.reply_text(answer.fulfillment_text)
    except NetworkError as error:
        logger.warning(f'Network error: {error}\n')
        sleep(10)


def main():
    env = Env()
    env.read_env()
    tg_token = env.str("TG_TOKEN")
    project_id = env.str("PROJECT_ID")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                           partial(reply_to_message, project_id=project_id)))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
