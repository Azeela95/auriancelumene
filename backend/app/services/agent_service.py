# app/services/agent_service.py
from typing import Dict, Any, List
from app.services.llm_service import LLMService

class HealthAgent:
    def __init__(self):
        self.context_memory = {}
        self.llm_service = LLMService()
        print("✅ Agent santé avec IA initialisé !")
    
    async def process_user_message(self, user_id: int, message: str, context: Dict = None) -> Dict[str, Any]:
        """
        Traite le message utilisateur avec IA
        """
        # Initialise la mémoire de contexte
        if user_id not in self.context_memory:
            self.context_memory[user_id] = {
                "conversation_history": [],
                "user_profile": {},
                "last_intent": None
            }
        
        # Construit le contexte pour l'IA
        chat_context = {
            "user_profile": self.context_memory[user_id]["user_profile"],
            "conversation_history": self.context_memory[user_id]["conversation_history"][-5:]  # Derniers 5 messages
        }
        
        # Appel à l'IA pour une réponse intelligente
        ai_response = await self.llm_service.generate_health_response(message, chat_context)
        
        # Met à jour l'historique
        self.context_memory[user_id]["conversation_history"].extend([
            {"role": "user", "message": message},
            {"role": "assistant", "message": ai_response}
        ])
        
        # Limite l'historique à 20 messages
        if len(self.context_memory[user_id]["conversation_history"]) > 20:
            self.context_memory[user_id]["conversation_history"] = self.context_memory[user_id]["conversation_history"][-20:]
        
        return {
            "answer": ai_response,
            "type": "ai_generated",
            "urgency": "low",
            "suggestions": self._generate_suggestions(message)
        }
    
    def _generate_suggestions(self, message: str) -> List[str]:
        """Génère des suggestions contextuelles"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["stress", "anxiété"]):
            return ["Exercice respiration", "Méditation guidée", "Conseil sommeil"]
        elif any(word in message_lower for word in ["sommeil", "fatigue"]):
            return ["Routine sommeil", "Conseil literie", "Relaxation"]
        elif any(word in message_lower for word in ["manger", "alimentation"]):
            return ["Recette santé", "Plan repas", "Conseil hydratation"]
        else:
            return ["Sommeil", "Nutrition", "Activité physique", "Santé mentale"]
    
    def get_conversation_history(self, user_id: int) -> List[Dict]:
        return self.context_memory.get(user_id, {}).get("conversation_history", [])
    
    def clear_conversation_history(self, user_id: int):
        if user_id in self.context_memory:
            self.context_memory[user_id]["conversation_history"] = []