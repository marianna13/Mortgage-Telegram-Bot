from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from classifier import get_tag
import os
from dotenv import load_dotenv

load_dotenv()

rates = {
    "для новостроек": [10.5, 0],
    "вторичного жилья": [10.5, 0],
    "для семей": [5.3, 15],
    "с государственной поддержкой": [6.3, 15],
}

api_key = os.environ["API_KEY"]

updater = Updater(api_key, use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🏠🤗Здравствуйте! Вас приветсвует Ипотечный бот! Введите категорию жилья, чтобы узнать размер ставки и первоначальный взнос. Если Вам нужна помощь используйте команду /help"
    )


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
        Напишите категорию жилья (например, 'новостройки') \n
        Команды:
        /start в начало
        /help помощь
        Подробнее => https://www.sberbank.ru/ru/person/credits/homenew
        """
    )


def unknown_text(update: Update, context: CallbackContext):
    message = update.message.text
    tag = get_tag(message)
    if tag == "not recognized":
        update.message.reply_text(
            "Извините, но я не понял, что вы хотели сказать. Используйте команду /help если вам нужна помощь."
        )
    else:
        rate, payement = rates[tag]
        response = f"Ставка: от {rate}%, первый взнос от {payement}% {tag}"
        update.message.reply_text(response)


if __name__ == "__main__":
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

    updater.start_polling()
