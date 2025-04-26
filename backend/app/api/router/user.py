from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette import status

from app.core.auth import create_access_token, decode_token, get_current_user
from app.core.db import get_db
from app.core.security import get_password_hash, verify_password
from app.core.time import utc_now
from app.models.User import UserCreate, UserResponse, UserInDB, UserRole

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db=Depends(get_db)):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user_data = {
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "role": UserRole.USER,
        "created_at": utc_now()
    }

    result = await db.users.insert_one(user_data)
    created_user = await db.users.find_one({"_id": result.inserted_id})

    created_user["id"] = str(created_user["_id"])
    created_user.pop("_id", None)
    created_user.pop("hashed_password", None)

    return created_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token_data = {"sub": user["email"], "user_id": str(user["_id"])}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserInDB)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user
