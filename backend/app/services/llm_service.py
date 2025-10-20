# app/services/llm_service.py
import os
import requests
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        print("✅ Service ChatGPT initialisé !")
    
    async def generate_health_response(self, user_message: str, context: Dict) -> str:
        """
        Utilise ChatGPT pour générer des réponses santé personnalisées
        """
        prompt = self._build_health_prompt(user_message, context)
        
        try:
            if self.api_key:
                # Appel réel à l'API ChatGPT
                response = await self._call_chatgpt_api(prompt)
                return self._validate_health_response(response)
            else:
                # Mode démo si pas de clé API
                return self._get_demo_response(user_message, context)
                
        except Exception as e:
            print(f"❌ Erreur ChatGPT: {e}")
            return self._get_fallback_response(user_message)
    
    def _build_health_prompt(self, user_message: str, context: Dict) -> str:
        """Construit un prompt sécurisé pour ChatGPT"""
        return f"""
        Tu es Auriance, un assistant santé bienveillant et prudent spécialisé dans l'accompagnement quotidien des patients et soignants.

        CONTEXTE UTILISATEUR: {context.get('user_profile', {})}
        HISTORIQUE CONVERSATION: {context.get('conversation_history', [])}
        DERNIER MESSAGE: {user_message}

        🔒 RÈGLES STRICTES À RESPECTER:
        - NE JAMAIS faire de diagnostic médical
        - NE JAMAIS recommander de médicaments spécifiques
        - Toujours orienter vers un professionnel de santé pour les symptômes sérieux
        - Donner des conseils généraux de bien-être basés sur des preuves scientifiques
        - Être empathique, encourageant et personnalisé
        - Répondre en français naturel et chaleureux
        - Limiter la réponse à 2-3 phrases maximum

        💡 DOMAINES D'EXPERTISE AUTORISÉS:
        - Hygiène de vie (sommeil, nutrition, activité physique)
        - Gestion du stress et bien-être mental
        - Conseils généraux de prévention
        - Accompagnement des habitudes santé

        🎯 TA RÉPONSE (ton professionnel et bienveillant):
        """
    
    async def _call_chatgpt_api(self, prompt: str) -> str:
        """Appel réel à l'API ChatGPT"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",  # ou "gpt-4" si tu as accès
            "messages": [
                {
                    "role": "system", 
                    "content": "Tu es un assistant santé bienveillant et prudent. Tu donnes des conseils généraux de bien-être sans jamais faire de diagnostic médical."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions", 
                headers=headers, 
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.Timeout:
            return "Désolé, le service est temporairement indisponible. Veuillez réessayer."
        except Exception as e:
            print(f"Erreur API ChatGPT: {e}")
            raise e
    
    def _get_demo_response(self, user_message: str, context: Dict) -> str:
        """Réponses intelligentes en mode démo (si pas d'API Key)"""
        message_lower = user_message.lower()
        
        demo_responses = {
            "stress": "Je comprends que le stress peut être éprouvant. La cohérence cardiaque (respiration 5-5-6) est une technique simple : inspirez 5s, expirez 5s, pendant 5 minutes. Cela peut aider à réguler le système nerveux. 🧘‍♀️",
            "sommeil": "Pour un sommeil réparateur, une routine régulière est clé. Chambre fraîche (18-20°C), obscurité totale, et pas d'écrans 1h avant le coucher peuvent faire une grande différence. 😴",
            "nutrition": "Une assiette équilibrée avec des légumes colorés, des protéines maigres et des céréales complètes est idéale. Pensez à varier les couleurs pour diversifier les nutriments ! 🥗",
            "exercice": "L'activité physique régulière est excellente pour la santé. Même 30 minutes de marche quotidienne peuvent améliorer l'humeur et l'énergie. Quel est votre niveau d'activité actuel ? 🚶‍♂️",
            "default": "Je suis là pour vous accompagner vers un meilleur bien-être. De quel aspect de votre santé aimeriez-vous parler ? (sommeil, nutrition, activité, gestion du stress...) 🌟"
        }
        
        if any(word in message_lower for word in ["stress", "anxiété", "nerveux"]):
            return demo_responses["stress"]
        elif any(word in message_lower for word in ["sommeil", "dormir", "nuit", "fatigue"]):
            return demo_responses["sommeil"]
        elif any(word in message_lower for word in ["manger", "aliment", "nourriture", "régime"]):
            return demo_responses["nutrition"]
        elif any(word in message_lower for word in ["exercice", "sport", "marche", "activité"]):
            return demo_responses["exercice"]
        else:
            return demo_responses["default"]
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Réponse de secours ultra-sécurisée"""
        return "Je comprends votre préoccupation. Pour des conseils personnalisés, je recommande de consulter un professionnel de santé. En attendant, je peux vous aider sur le bien-être général et les habitudes santé. 🌿"
    
    def _validate_health_response(self, response: str) -> str:
        """Valide que la réponse est sécuritaire"""
        forbidden_terms = ["diagnostic", "médicament", "prescrire", "guérir", "maladie"]
        if any(term in response.lower() for term in forbidden_terms):
            return "Je vous recommande de consulter un professionnel de santé pour une évaluation personnalisée. Je peux vous aider sur les aspects bien-être et prévention. 🩺"
        return response