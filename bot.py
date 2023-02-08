import logging
from functools import partial
from time import sleep

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.error import NetworkError
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


LANGUAGE_CODE='ru-RU'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response.query_result


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

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, partial(reply_to_message, project_id=project_id)))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
