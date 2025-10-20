# app/api/routes/gamification_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

router = APIRouter(prefix="/gamification", tags=["Health Gamification"])

class QuestCompletion(BaseModel):
    user_id: int
    quest_id: str
    completion_data: Dict[str, Any]

class HealthQuest(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    rewards: Dict[str, int]
    requirements: List[str]

@router.get("/quests/{user_id}")
async def get_user_quests(user_id: int):
    """
    Récupère les quêtes santé personnalisées d'un utilisateur
    """
    try:
        quests = await _generate_personalized_quests(user_id)
        return {
            "user_id": user_id,
            "active_quests": quests["active"],
            "completed_quests": quests["completed"],
            "available_quests": quests["available"],
            "user_level": quests["level"],
            "total_xp": quests["xp"]
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur récupération quêtes: {str(e)}")

@router.post("/complete-quest")
async def complete_quest(completion: QuestCompletion):
    """
    Marque une quête comme complétée et attribue les récompenses
    """
    try:
        result = await _process_quest_completion(completion)
        return {
            "status": "success",
            "quest_completed": completion.quest_id,
            "rewards_earned": result["rewards"],
            "level_up": result["level_up"],
            "new_level": result["new_level"]
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur complétion quête: {str(e)}")

@router.get("/leaderboard")
async def get_health_leaderboard():
    """
    Classement bien-être des utilisateurs (anonyme)
    """
    try:
        leaderboard = await _generate_leaderboard()
        return {
            "leaderboard": leaderboard,
            "timeframe": "monthly",
            "total_participants": len(leaderboard)
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur génération classement: {str(e)}")

@router.get("/rewards/{user_id}")
async def get_user_rewards(user_id: int):
    """
    Récupère les récompenses et badges de l'utilisateur
    """
    try:
        rewards = await _get_user_rewards_data(user_id)
        return {
            "user_id": user_id,
            "badges": rewards["badges"],
            "achievements": rewards["achievements"],
            "total_points": rewards["points"],
            "next_reward": rewards["next_reward"]
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur récupération récompenses: {str(e)}")

async def _generate_personalized_quests(user_id: int) -> Dict[str, Any]:
    """Génère des quêtes santé personnalisées"""
    return {
        "active": [
            {
                "id": "hydration_master",
                "title": "Maître de l'Hydratation 💧",
                "description": "Boire 2L d'eau pendant 7 jours consécutifs",
                "progress": 0.6,
                "deadline": "2024-01-22"
            }
        ],
        "completed": ["sleep_warrior", "meditation_beginner"],
        "available": ["stress_slayer", "nutrition_ninja"],
        "level": 5,
        "xp": 1250
    }

async def _process_quest_completion(completion: QuestCompletion) -> Dict[str, Any]:
    """Traite la complétion d'une quête"""
    return {
        "rewards": {"xp": 100, "badge": "quest_completer"},
        "level_up": True,
        "new_level": 6
    }

async def _generate_leaderboard() -> List[Dict[str, Any]]:
    """Génère le classement bien-être"""
    return [
        {"rank": 1, "username": "***123", "score": 980, "level": 10},
        {"rank": 2, "username": "***456", "score": 850, "level": 8},
        {"rank": 3, "username": "***789", "score": 720, "level": 7}
    ]

async def _get_user_rewards_data(user_id: int) -> Dict[str, Any]:
    """Récupère les récompenses utilisateur"""
    return {
        "badges": ["early_riser", "hydration_king", "meditation_master"],
        "achievements": ["7_days_streak", "first_quest"],
        "points": 1250,
        "next_reward": "zen_master à 1500 points"
    }