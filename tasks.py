import logging
from aiogram import Bot
from taskiq_aio_pika import AioPikaBroker

from config import (
    BOT_TOKEN,
    TELEGRAM_USER_ID,
    get_rabbitmq_url,
)

log = logging.getLogger(__name__)

# Initialize taskiq broker with result backend
broker = AioPikaBroker(
    get_rabbitmq_url(),
    max_priority=10,
)

# Initialize bot
bot = Bot(token=BOT_TOKEN)


@broker.task(retry_on_error=True, max_retries=5)
async def send_telegram_message(message_text: str) -> dict:
    """
    Task to send a message to Telegram user
    
    Args:
        message_text: Text message to send
        
    Returns:
        dict with status and details
        
    Raises:
        Exception: If sending fails, task will be retried up to 5 times
    """
    try:
        result = await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message_text)
        log.info("Sent message to Telegram user %s: %s", TELEGRAM_USER_ID, message_text)
        return {
            "status": "success",
            "message_id": result.message_id,
            "text": message_text
        }
    except Exception as e:
        log.error("Failed to send message to Telegram: %s", e)
        # Raise exception to trigger retry
        raise
