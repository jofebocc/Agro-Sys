from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

from app.core.time import utc_now


# Helper for ObjectId compatibility
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# Base company attributes common to create/update
class CompanyBase(BaseModel):
    name: str
    location: Optional[str]
    phone: str
    email: EmailStr

# For creating a new company (client-side input)
class CompanyCreate(CompanyBase):
    pass  # add extra fields if needed specifically for creation

# For updating an existing company (all fields optional)
class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    updated_at: datetime = Field(default_factory=utc_now)

# Company model retrieved from DB
class CompanyInDB(CompanyBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,  # <-- replaces allow_population_by_field_name
        "arbitrary_types_allowed": True
    }

# Public response model (exposed in APIs)
class CompanyResponse(CompanyBase):
    id: str
    created_at: datetime
    updated_at: datetime