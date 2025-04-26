from fastapi import APIRouter
from app.api.router import company, user

api_router = APIRouter()

api_router.include_router(company.router)
api_router.include_router(user.router)