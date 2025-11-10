import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aio_pika import connect_robust, Message

from config import (
    get_rabbitmq_url,
    configure_logging,
    MQ_ROUTING_KEY,
)

log = logging.getLogger(__name__)

app = FastAPI(title="RabbitMQ API")


class MessageRequest(BaseModel):
    text: str


@app.post("/send-message")
async def send_message(request: MessageRequest):
    """Send a message to RabbitMQ queue"""
    try:
        connection = await connect_robust(get_rabbitmq_url())
        
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(MQ_ROUTING_KEY)
            
            await channel.default_exchange.publish(
                Message(body=request.text.encode()),
                routing_key=MQ_ROUTING_KEY,
            )
            
            log.info("Published message to RabbitMQ: %s", request.text)
            return {"status": "success", "message": f"Message sent: {request.text}"}
    
    except Exception as e:
        log.error("Failed to publish message: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    configure_logging(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
