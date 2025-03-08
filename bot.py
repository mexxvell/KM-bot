
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)
from constants import MESSAGES
from web_server import keep_alive

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
CALCULATING = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка команды /start."""
    user = update.effective_user
    await update.message.reply_text(
        MESSAGES['start'],
        reply_markup=ReplyKeyboardMarkup([["Рассчитать стоимость"]], resize_keyboard=True)
    )
    return CALCULATING

async def handle_calculation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка расчета."""
    await update.message.reply_text(
        "✅ Расчет завершен!\nИтоговая стоимость: 1 000 000 ₽",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога."""
    await update.message.reply_text(MESSAGES['cancel'], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main() -> None:
    """Запуск бота."""
    # Получение токена из переменных окружения
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logger.error("Не найден токен Telegram. Установите переменную окружения TELEGRAM_TOKEN.")
        return
    
    keep_alive()  # Активируем веб-сервер
    
    application = Application.builder().token(token).build()

    # Настройка обработчиков
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^Рассчитать стоимость$"), handle_calculation)
        ],
        states={
            CALCULATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_calculation)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
