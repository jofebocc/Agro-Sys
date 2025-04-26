from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.core.time import utc_now

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.USER

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    role: UserRole
    created_at: datetime = Field(default_factory=utc_now)

class UserResponse(UserBase):
    id: str
    role: UserRole
    created_at: datetime
