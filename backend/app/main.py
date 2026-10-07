import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)


from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import webhook,phone_number

from models.entity.users import Users
from models.entity.conversations import Conversations
from models.entity.phone_numbers import PhoneNumbers
from models.entity.messages import Messages
from models.entity.message_status import MessageStatus
from database.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting up the server...")

    init_db()      # Create the database tables

    yield

    logging.info("Shutting down the server...")



# Create the app
app = FastAPI(title="WhatsApp MCP Server",redirect_slashes=False)


# Register routers
app.include_router(webhook.router,prefix='/api/v1/webhook', tags=["webhook"])
app.include_router(phone_number.router,prefix='/api/v1/phone_number', tags=["phone_number"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")