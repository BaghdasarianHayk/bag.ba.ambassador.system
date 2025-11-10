import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import configure_logging
from tasks import send_telegram_message

log = logging.getLogger(__name__)

app = FastAPI(title="RabbitMQ API")


class MessageRequest(BaseModel):
    text: str


@app.post("/send-message")
async def send_message(request: MessageRequest):
    """Send a message via taskiq to Telegram"""
    try:
        # Kick off the task asynchronously
        task = await send_telegram_message.kiq(request.text)
        
        log.info("Queued message task: %s", request.text)
        return {
            "status": "success",
            "message": f"Message queued: {request.text}",
            "task_id": task.task_id
        }
    
    except Exception as e:
        log.error("Failed to queue message: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    configure_logging(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)
