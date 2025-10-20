# app/api/routes/planning_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.planning import Planning

router = APIRouter(prefix="/plannings", tags=["Plannings"])

@router.get("/")
def get_all_plannings(db: Session = Depends(get_db)):
    return db.query(Planning).all()

@router.get("/{planning_id}")
def get_planning(planning_id: int, db: Session = Depends(get_db)):
    planning = db.query(Planning).filter(Planning.id == planning_id).first()
    if not planning:
        raise HTTPException(status_code=404, detail="Planning non trouvé")
    return planning
