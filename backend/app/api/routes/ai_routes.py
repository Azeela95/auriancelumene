# app/api/routes/ai_routes.py
from fastapi import APIRouter
from app.models.recommendation import Recommendation

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/recommend")
def get_recommendation(user_input: str):
    """
    Exemple simple — on remplacera plus tard par ton moteur IA.
    """
    if "stress" in user_input.lower():
        return {"recommendation": "Faites 10 minutes de respiration consciente 🧘‍♀️"}
    elif "fatigue" in user_input.lower():
        return {"recommendation": "Essayez de dormir 8h cette nuit 😴"}
    else:
        return {"recommendation": "Buvez de l’eau et marchez un peu 💧🚶"}
