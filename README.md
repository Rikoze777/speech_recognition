# speech_recognition

Приложение для запуска ботов Telegram и ВК, обученных в DialogFlow отвечать на вопросы.

![tg](https://user-images.githubusercontent.com/61386361/218321093-6deb7475-c5d1-46c4-9fe7-1375615d772f.gif)

![vk](https://user-images.githubusercontent.com/61386361/218321096-a2413f63-ed7a-4e57-899f-be78f2996de8.gif)


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

## Обучение бота:
* Сначала, добавьте необходимые вопросы и ответы как это сделано `questions.json`
* Запустите следующий скрипт:
```
python3 dialogflow_training.py
```

## Запуск бота
* Telegram бот
```
python3 tg_bot.py
```
* ВК бот
```
python3 vk_bot.py
```
