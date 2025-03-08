from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text('Hello! I am your bot.')

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    TOKEN = '7575688103:AAFLwPlKHuNLBPUv5VnBupzVe_1W6SNf1zc'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
