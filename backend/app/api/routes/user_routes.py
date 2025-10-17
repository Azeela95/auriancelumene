from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.user_service import create_user, get_users

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

@router.post("/", summary="Create a user")
def add_user(user: UserCreate):
    # basic checks (unique constraint handled by DB)
    res = create_user(user.username, user.email, user.password)
    return res

@router.get("/", summary="List users")
def list_users():
    users = get_users()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]
