import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import (
    BOT_TOKEN,
    WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBAPP_HOST,
    WEBAPP_PORT,
    configure_logging,
)

log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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
