import logging

RMQ_HOST = "localhost"
RMQ_PORT = 5672

RMQ_USER = "guest"
RMQ_PASSWORD = "guest"

MQ_EXCHANGE = ""
MQ_ROUTING_KEY = "news"

# Telegram Bot Configuration
BOT_TOKEN = "8497899812:AAEO3PabXI5NPLkDLLo2yR6bNIF01XgUCgc"
TELEGRAM_USER_ID = 796973748  # Replace with your Telegram user ID
WEBHOOK_HOST = "https://owkya-78-109-72-68.a.free.pinggy.link"
WEBHOOK_PATH = "/bots/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Webhook server configuration
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = 8080

# FastAPI server configuration
API_HOST = "0.0.0.0"
API_PORT = 8000


def get_rabbitmq_url() -> str:
    return f"amqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_HOST}:{RMQ_PORT}/"


def configure_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
    )
