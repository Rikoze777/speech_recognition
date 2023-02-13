import logging

from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    client = dialogflow.SessionsClient()
    session = client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result


class LogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)