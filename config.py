import logging

RMQ_HOST = "0.0.0.0"
RMQ_PORT = 5672

RMQ_USER = "guest"
RMQ_PASSWORD = "guest"

MQ_EXCHANGE = ""
MQ_ROUTING_KEY = "news"


def get_rabbitmq_url() -> str:
    return f"amqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_HOST}:{RMQ_PORT}/"


def configure_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s",
    )
