from flask import Flask, request, jsonify
from threading import Thread
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os

app = Flask(__name__)

# Initialize the bot with your token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("No token provided. Please set the TELEGRAM_BOT_TOKEN environment variable.")
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'ok'
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def start(update, context):
    update.message.reply_text('Hello! I am your bot.')

def echo(update, context):
    update.message.reply_text(update.message.text)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run, daemon=True).start()

# Set up the dispatcher and handlers
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Set the webhook
bot.set_webhook(url='https://your_domain.com/webhook')