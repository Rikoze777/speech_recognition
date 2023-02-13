import logging
import sys
from random import randint
from time import sleep

import telegram
import vk_api as vk
from environs import Env
from requests.exceptions import ConnectionError
from vk_api.longpoll import VkEventType, VkLongPoll

from misc_tools import LogsHandler, detect_intent_texts


LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger(__name__)


def reply_message(event, vk_api, project_id):
    session_id = f'vk-{event.user_id}'
    answer = detect_intent_texts(
        project_id, session_id, event.text, LANGUAGE_CODE)
    if not answer.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer.fulfillment_text,
            random_id=randint(1, 100000)
        )


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    vk_token = env.str('VK_TOKEN')
    tg_token = env.str('TG_TOKEN')
    user_id = env.str('USER_ID')
    bot = telegram.Bot(token=tg_token)
    logging.basicConfig(
        filename='vk_app.log',
        filemode='w',
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(asctime)s - %(message)s'
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    logger.addHandler(LogsHandler(bot, user_id))
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply_message(event, vk_api, project_id)
        except ConnectionError as error:
            logger.warning(f'Connection error: {error}\n')
            sleep(20)


if __name__ == '__main__':
    main()
