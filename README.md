# speech_recognition

Приложение для запуска ботов Telegram и ВК, обученных в DialogFlow отвечать на вопросы.


## Установка

1) Клонировать проект:
```
git clone https://github.com/Rikoze777/speech_recognition.git
```

2) Установить зависимости:
```
pip install -r requiremenets.txt
```

3) Создать .env файл для ваших секретных ключей:
```
touch .env
```

4) Записать в .env следующие переменные:
* TG_TOKEN='Ваш телеграм токен'  [Получают при создании у отца ботов](https://t.me/botfather)
* PROJECT_ID='Ваш ID проекта' Создайте проект [тут](https://dialogflow.cloud.google.com/#/editAgent), после перейдите по ID для связывания проекта с cloud
* USER_ID='ID вашей личной страницы Telegram' [узнать можно тут](https://t.me/username_to_id_bot)
* VK_TOKEN='Токен вашей группы ВК' Не забудьте также разрешить отправление сообщений группе


5) Настройка DialogFlow:
* [Выполнить данную инструкцию](https://cloud.google.com/sdk/docs/install-sdk)
* [Разрешить API](https://cloud.google.com/dialogflow/es/docs/quick/setup)
* Созданный .json файл с данными (по умолчанию в /.config/gcloud) переименовать в 'credentials.json'

6) Обучение бота:
* Сначала, добавьте необходимые вопросы и ответы как это сделано `questions.json`
* Запустите следующий скрипт:
```
python3 dialogflow_training.py
```

7) Запустить бота
Telegram бот
```
python3 tg_bot.py
```
или ВК бота
```
python3 vk_bot.py
```