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
- `consumer.py` - Taskiq worker that processes tasks
- `tasks.py` - Taskiq tasks definition (send Telegram messages)
- `bot.py` - Telegram bot with webhook (minimal setup)
- `api.py` - FastAPI server with endpoint to queue tasks
- `config.py` - Configuration file

## Running the Application

1. Start RabbitMQ:
```bash
docker-compose up -d
```

2. Start the taskiq worker (consumer):
```bash
python consumer.py
```

3. Start the FastAPI server:
```bash
python api.py
```

4. Send a message via API:
```bash
curl -X POST http://localhost:8000/send-message \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from API!"}'
```

The taskiq worker will process the task and send the message to the configured Telegram user.

