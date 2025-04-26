import logging
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

from fastapi import FastAPI
from fastapi.params import Depends

from app.api.main import api_router
from app.core.db import get_db
from app.core.init_admin import create_initial_admin

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(name=__name__)

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Database setup explicitly
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    app.state.db = db

    # Check DB connection explicitly and clearly
    ping_response = await db.command("ping")
    if ping_response.get("ok") != 1:
        raise Exception("Database connection failed")

    # Create initial admin explicitly with the correct DB instance
    await create_initial_admin(db)

    print("🚀 Application startup completed.")

    yield  # Application runs explicitly here.

    # Teardown explicitly
    client.close()
    print("🔻 Application shutdown completed.")
app = FastAPI(
    title="Agro-Sys",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

@app.get("/test-db")
async def test_db(db=Depends(get_db)):
    try:
        await db.command("ping")
        return {"status": "MongoDB connected successfully!"}
    except Exception as e:
        return {"status": f"Error: {str(e)}"}
