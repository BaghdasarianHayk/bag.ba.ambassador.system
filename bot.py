import asyncio
import time
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aio_pika import connect_robust, Message

from config import (
    BOT_TOKEN,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBAPP_HOST,
    WEBAPP_PORT,
    get_rabbitmq_url,
    configure_logging,
    MQ_ROUTING_KEY,
)

log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def publish_message_to_rabbitmq(message_text: str):
    """Publish a message to RabbitMQ"""
    connection = await connect_robust(get_rabbitmq_url())
    
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(MQ_ROUTING_KEY)
        
        await channel.default_exchange.publish(
            Message(body=message_text.encode()),
            routing_key=MQ_ROUTING_KEY,
        )
        log.info("Published message to RabbitMQ: %s", message_text)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle /start command - publish a message to RabbitMQ"""
    message_body = f"Hello World from {time.time()}"
    
    try:
        await publish_message_to_rabbitmq(message_body)
        await message.answer(f"✅ Message published to RabbitMQ:\n{message_body}")
        log.warning("Published message via bot: %s", message_body)
    except Exception as e:
        log.error("Failed to publish message: %s", e)
        await message.answer(f"❌ Failed to publish message: {e}")


async def on_startup():
    """Set webhook on startup"""
    await bot.set_webhook(WEBHOOK_URL)
    log.warning("Webhook set to: %s", WEBHOOK_URL)


async def on_shutdown():
    """Delete webhook on shutdown"""
    await bot.delete_webhook()
    log.warning("Webhook deleted")


def main():
    configure_logging(level=logging.WARNING)
    
    # Create aiohttp application
    app = web.Application()
    
    # Setup webhook handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    
    # Setup startup and shutdown hooks
    app.on_startup.append(lambda _: on_startup())
    app.on_shutdown.append(lambda _: on_shutdown())
    
    # Setup application
    setup_application(app, dp, bot=bot)
    
    log.warning("Starting webhook server on %s:%s", WEBAPP_HOST, WEBAPP_PORT)
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
