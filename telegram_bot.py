
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text('Hello! I am your bot.')

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Ошибка: Не найден токен Telegram. Установите переменную окружения TELEGRAM_TOKEN.")
        return
        
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
