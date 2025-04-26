from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env file

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "AgroSys")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

# Helper function (optional but useful)
async def get_db():
    return db