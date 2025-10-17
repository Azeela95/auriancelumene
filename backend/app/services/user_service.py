from app.models.user import User
from app.core.database import SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(username: str, email: str, password: str):
    db = SessionLocal()
    try:
        hashed_pw = get_password_hash(password)
        user = User(username=username, email=email, hashed_password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User created", "user": {"id": user.id, "username": user.username, "email": user.email}}
    finally:
        db.close()

def get_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()
