# app/api/routes/patient_routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.patient import Patient

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/")
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient non trouvé")
    return patient
