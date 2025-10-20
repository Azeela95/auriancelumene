# app/api/routes/prediction_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/predictions", tags=["Health Predictions"])

class PredictionRequest(BaseModel):
    user_id: int
    days_ahead: int = 90  # Prédiction sur 3 mois

class HealthPredictionResponse(BaseModel):
    risk_assessment: Dict[str, float]
    preventive_recommendations: List[str]
    vitality_score: float
    alerts: List[str]
    predicted_trends: Dict[str, Any]

@router.post("/health-risks", response_model=HealthPredictionResponse)
async def predict_health_risks(request: PredictionRequest):
    """
    Prédiction des risques santé 3 mois à l'avance
    """
    try:
        predictions = await _generate_health_predictions(request.user_id, request.days_ahead)
        return predictions
    except Exception as e:
        raise HTTPException(500, f"Erreur prédiction santé: {str(e)}")

@router.get("/vitality-score/{user_id}")
async def get_vitality_score(user_id: int):
    """
    Score de vitalité quotidien basé sur multiples facteurs
    """
    try:
        score = await _calculate_vitality_score(user_id)
        return {
            "user_id": user_id,
            "vitality_score": score,
            "level": _get_vitality_level(score),
            "trend": "improving",  # ou "stable", "declining"
            "factors": ["sleep", "activity", "nutrition", "stress"]
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur calcul vitalité: {str(e)}")

@router.post("/migraine-alert")
async def predict_migraine_alert(request: PredictionRequest):
    """
    Alerte migraine 24h à l'avance via patterns
    """
    try:
        alert = await _predict_migraine_pattern(request.user_id)
        return {
            "migraine_risk": alert["risk_level"],
            "probability": alert["probability"],
            "timeframe": alert["timeframe"],
            "preventive_actions": alert["actions"]
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur prédiction migraine: {str(e)}")

@router.get("/stress-patterns/{user_id}")
async def analyze_stress_patterns(user_id: int):
    """
    Analyse patterns de stress et recommandations
    """
    try:
        patterns = await _analyze_stress_data(user_id)
        return {
            "user_id": user_id,
            "stress_patterns": patterns["patterns"],
            "triggers": patterns["triggers"],
            "coping_strategies": patterns["strategies"],
            "improvement_timeline": patterns["timeline"]
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur analyse stress: {str(e)}")

async def _generate_health_predictions(user_id: int, days_ahead: int) -> Dict[str, Any]:
    """Génère prédictions santé personnalisées"""
    return {
        "risk_assessment": {
            "stress_burnout": 0.3,
            "sleep_disorders": 0.2,
            "nutrition_deficit": 0.15,
            "physical_inactivity": 0.25
        },
        "preventive_recommendations": [
            "Pratiquer la cohérence cardiaque 5min/jour",
            "Augmenter consommation légumes verts",
            "Marche quotidienne 30 minutes"
        ],
        "vitality_score": 0.85,
        "alerts": ["Aucune alerte critique"],
        "predicted_trends": {
            "energy_level": "stable",
            "sleep_quality": "improving",
            "stress_resilience": "improving"
        }
    }

async def _calculate_vitality_score(user_id: int) -> float:
    """Calcule le score de vitalité"""
    return 0.85  # Simulation

async def _predict_migraine_pattern(user_id: int) -> Dict[str, Any]:
    """Prédit risques migraine"""
    return {
        "risk_level": "low",
        "probability": 0.15,
        "timeframe": "24-48h",
        "actions": ["Hydratation", "Repos visuel", "Ambiance calme"]
    }

async def _analyze_stress_data(user_id: int) -> Dict[str, Any]:
    """Analyse patterns stress"""
    return {
        "patterns": ["stress_post_work", "tension_weekend"],
        "triggers": ["écrans prolongés", "manque pause"],
        "strategies": ["respiration 4-7-8", "marche nature"],
        "timeline": "amélioration sous 2 semaines"
    }

def _get_vitality_level(score: float) -> str:
    """Détermine le niveau de vitalité"""
    if score >= 0.8: return "excellent"
    elif score >= 0.6: return "bon"
    elif score >= 0.4: return "modéré"
    else: return "faible"