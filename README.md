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
- `consumer.py` - Message consumer that sends messages to Telegram user
- `bot.py` - Telegram bot with webhook that publishes messages on /start command
- `api.py` - FastAPI server with endpoint to publish messages to RabbitMQ
- `config.py` - Configuration file

## API Usage

Start the FastAPI server:
```bash
python api.py
```

Send a message via API:
```bash
curl -X POST http://localhost:8000/send-message \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from API!"}'
```

The consumer will receive the message and send it to the configured Telegram user.

