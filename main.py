
import logging
import os
from bot import main as bot_main
from web_server import keep_alive

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Проверка наличия токена
    if not os.getenv("TELEGRAM_TOKEN"):
        logger.warning("Токен Telegram не найден в переменных окружения!")
        logger.info("Пожалуйста, добавьте TELEGRAM_TOKEN в Replit Secrets.")
    
    # Запуск веб-сервера для поддержания работы бота
    keep_alive()
    
    # Запуск бота
    bot_main()
