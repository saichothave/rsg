
from os import getenv
from telegram import Bot
from datetime import datetime
from django.utils import timezone




async def send_document_async(buffer, filename, caption):
    # Your Telegram bot token and chat ID
    TELEGRAM_BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID')

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_document(
        chat_id=TELEGRAM_CHAT_ID,
        document=buffer,
        filename=filename,
        caption=caption
    )