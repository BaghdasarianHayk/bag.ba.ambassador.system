import asyncio
import time
import logging

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractIncomingMessage

from config import (
    get_rabbitmq_url,
    configure_logging,
    MQ_ROUTING_KEY,
)

log = logging.getLogger(__name__)


async def process_new_message(message: AbstractIncomingMessage):
    async with message.process():
        log.debug("message: %s", message)
        log.debug("body: %s", message.body)

        log.warning("[ ] Start processing message (expensive task!) %r", message.body)
        start_time = time.time()
        ...
        await asyncio.sleep(1)
        ...
        end_time = time.time()
        log.info("Finished processing message %r, sending ack!", message.body)
        log.warning(
            "[X] Finished in %.2fs processing message %r",
            end_time - start_time,
            message.body,
        )


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
