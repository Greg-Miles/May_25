import os
import asyncio
from telegram import Bot # poetry add python-telegram-bot
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
async def send_telegram_message(token, chat_id, text:str, parse_mode="Markdown"):
    """
    Фукция отправляет сообщение в Telegram.
    :param token: Токен бота Telegram.
    :param chat_id: Идентификатор чата, куда будет отправлено сообщение.
    :param text: Текст сообщения.
    """

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode=parse_mode)
        logging.info(f"Сообщение отправлено в Telegram: {text}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")
        raise

if __name__ == "__main__":
    message = "Тестовое сообщение"
    asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message))