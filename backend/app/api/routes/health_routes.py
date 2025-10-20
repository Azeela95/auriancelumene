# app/api/routes/health_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.habitude import Habitude

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/habitudes")
def get_all_habitudes(db: Session = Depends(get_db)):
    return db.query(Habitude).all()

@router.post("/habitudes")
def create_habitude(user_id: int, name: str, db: Session = Depends(get_db)):
    hab = Habitude(user_id=user_id, name=name)
    db.add(hab)
    db.commit()
    db.refresh(hab)
    return hab
