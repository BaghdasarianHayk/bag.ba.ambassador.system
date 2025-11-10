# RabbitMQ Python Async Examples

This project uses aio-pika for async RabbitMQ operations and aiogram for Telegram bot integration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your bot token in `config.py`:
   - Set `BOT_TOKEN` to your Telegram bot token (get it from @BotFather)
   - Set `WEBHOOK_HOST` to your public domain (e.g., https://yourdomain.com)

3. Start RabbitMQ:
```bash
docker-compose up -d
```

4. Run the consumer:
```bash
python consumer.py
```

5. Run the bot (webhook mode):
```bash
python bot.py
```

6. Send `/start` command to your bot to publish a message to RabbitMQ

## Components

- `publisher.py` - Standalone message publisher
- `consumer.py` - Message consumer
- `bot.py` - Telegram bot with webhook that publishes messages on /start command
- `config.py` - Configuration file

