import os

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.security import get_password_hash
from app.core.time import utc_now
from app.models.User import UserRole
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
print("Loaded ADMIN_USERNAME:", ADMIN_USERNAME)
print("Loaded ADMIN_PASSWORD:", ADMIN_PASSWORD)

async def create_initial_admin(db: AsyncIOMotorDatabase):
    admin_email = str(ADMIN_USERNAME)
    admin_password = str(ADMIN_PASSWORD)

    existing_admin = await db.users.find_one({"email": ADMIN_USERNAME})

    if existing_admin:
        print("✅ Initial admin user already exists.")
        return

    admin_user = {
        "email": admin_email,
        "hashed_password": get_password_hash(ADMIN_PASSWORD),
        "role": UserRole.ADMIN.value,
        "created_at": utc_now()
    }

    await db.users.insert_one(admin_user)
    print("🚀 Initial admin user created successfully!")
