import asyncio
import time
import logging

from aiogram import Bot
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage

from config import (
    BOT_TOKEN,
    TELEGRAM_USER_ID,
    get_rabbitmq_url,
    configure_logging,
    MQ_ROUTING_KEY,
)

log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)


async def process_new_message(message: AbstractIncomingMessage):
    log.debug("message: %s", message)
    log.debug("body: %s", message.body)

    log.warning("[ ] Start processing message (expensive task!) %r", message.body)
    start_time = time.time()
    
    # Send message to Telegram user
    try:
        message_text = message.body.decode()
        await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message_text)
        log.info("Sent message to Telegram user %s: %s", TELEGRAM_USER_ID, message_text)
        
        # Acknowledge message only if successfully sent
        await message.ack()
        end_time = time.time()
        log.info("Finished processing message %r, sent ack!", message.body)
        log.warning(
            "[X] Finished in %.2fs processing message %r",
            end_time - start_time,
            message.body,
        )
    except Exception as e:
        log.error("Failed to send message to Telegram: %s", e)
        # Reject message and requeue it
        await message.reject(requeue=True)
        log.warning("Message rejected and requeued: %r", message.body)


async def consume_messages():
    connection = await connect_robust(get_rabbitmq_url())
    log.info("Created connection: %s", connection)
    
    async with connection:
        channel = await connection.channel()
        log.info("Created channel: %s", channel)
        
        queue = await channel.declare_queue(MQ_ROUTING_KEY)
        log.info("Declared queue: %s", queue)
        
        await queue.consume(process_new_message)
        log.warning("Waiting for messages...")
        
        await asyncio.Future()


def main():
    configure_logging(level=logging.WARNING)
    asyncio.run(consume_messages())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
