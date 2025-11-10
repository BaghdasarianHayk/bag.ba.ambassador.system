import asyncio
import time
import logging

from aio_pika import connect_robust, Message

from config import (
    get_rabbitmq_url,
    configure_logging,
    MQ_EXCHANGE,
    MQ_ROUTING_KEY,
)

log = logging.getLogger(__name__)


async def produce_message():
    connection = await connect_robust(get_rabbitmq_url())
    log.info("Created connection: %s", connection)
    
    async with connection:
        channel = await connection.channel()
        log.info("Created channel: %s", channel)
        
        queue = await channel.declare_queue(MQ_ROUTING_KEY)
        log.info("Declared queue %r %s", MQ_ROUTING_KEY, queue)
        
        message_body = f"Hello World from {time.time()}"
        log.info("Publish message %s", message_body)
        
        await channel.default_exchange.publish(
            Message(body=message_body.encode()),
            routing_key=MQ_ROUTING_KEY,
        )
        log.warning("Published message %s", message_body)


def main():
    configure_logging(level=logging.WARNING)
    asyncio.run(produce_message())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
