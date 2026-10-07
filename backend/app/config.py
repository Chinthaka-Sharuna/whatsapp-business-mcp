from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    DATABASE_URL = "postgresql+psycopg2://sharuna:12345678@localhost/whatsapp_mcp"