from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.habitude import Habitude

router = APIRouter()

# Dépendance pour récupérer la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ajouter une habitude
@router.post("/add")
def add_habitude(user_id: int, type_habitude: str, description: str = "", db: Session = Depends(get_db)):
    habitude = Habitude(user_id=user_id, type_habitude=type_habitude, description=description)
    db.add(habitude)
    db.commit()
    db.refresh(habitude)
    return {"message": "Habitude ajoutée", "habitude": habitude.id}

# Récupérer toutes les habitudes d’un utilisateur
@router.get("/{user_id}")
def get_habitudes(user_id: int, db: Session = Depends(get_db)):
    habitudes = db.query(Habitude).filter(Habitude.user_id == user_id).all()
    return habitudes

# Mettre à jour une habitude
@router.put("/update/{habitude_id}")
def update_habitude(habitude_id: int, type_habitude: str = None, description: str = None, db: Session = Depends(get_db)):
    habitude = db.query(Habitude).get(habitude_id)
    if not habitude:
        raise HTTPException(status_code=404, detail="Habitude non trouvée")
    if type_habitude:
        habitude.type_habitude = type_habitude
    if description:
        habitude.description = description
    db.commit()
    db.refresh(habitude)
    return {"message": "Habitude mise à jour", "habitude": habitude.id}

# Supprimer une habitude
@router.delete("/delete/{habitude_id}")
def delete_habitude(habitude_id: int, db: Session = Depends(get_db)):
    habitude = db.query(Habitude).get(habitude_id)
    if not habitude:
        raise HTTPException(status_code=404, detail="Habitude non trouvée")
    db.delete(habitude)
    db.commit()
    return {"message": "Habitude supprimée"}
