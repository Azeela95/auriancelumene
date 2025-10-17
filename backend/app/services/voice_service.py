# app/services/voice_service.py
import whisper
import tempfile
import os
from typing import Dict, Any

class VoiceService:
    def __init__(self):
        self.model = whisper.load_model("base")
        print("✅ Service Vocal initialisé !")
    
    async def transcribe_audio(self, audio_file) -> Dict[str, Any]:
        """
        Transcription audio avec analyse basique
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            content = await audio_file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Transcription avec Whisper
            print("🎤 Début de la transcription...")
            result = self.model.transcribe(tmp_path)
            
            # Analyse basique du contenu
            analysis = self._basic_analysis(result["text"])
            
            return {
                "text": result["text"],
                "language": result["language"],
                "confidence": result.get("confidence", 0.0),
                "analysis": analysis,
                "intent": self._detect_intent(result["text"])
            }
            
        except Exception as e:
            print(f"❌ Erreur transcription: {e}")
            raise e
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def _basic_analysis(self, text: str) -> Dict[str, Any]:
        """Analyse basique sans LLM"""
        if not text.strip():
            return {"urgency": "low", "category": "general"}
        
        text_lower = text.lower()
        
        urgency = "low"
        category = "general"
        
        # Détection d'urgence basique
        urgent_terms = ["urgence", "grave", "douleur intense", "saignement", "étouffe"]
        if any(term in text_lower for term in urgent_terms):
            urgency = "high"
        
        # Catégorisation basique
        if any(term in text_lower for term in ["sommeil", "dormir", "nuit", "insomnie"]):
            category = "sleep"
        elif any(term in text_lower for term in ["manger", "aliment", "nourriture", "faim"]):
            category = "nutrition" 
        elif any(term in text_lower for term in ["stress", "anxiété", "nerveux", "panique"]):
            category = "stress"
        elif any(term in text_lower for term in ["exercice", "sport", "marche", "entraînement"]):
            category = "exercise"
        elif any(term in text_lower for term in ["triste", "déprimé", "heureux", "émotion"]):
            category = "mental"
        
        return {
            "urgency": urgency,
            "category": category,
            "needs_followup": urgency in ["medium", "high"]
        }
    
    def _detect_intent(self, text: str) -> str:
        """Détecte l'intention du message vocal"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["conseil", "recommande", "suggestion"]):
            return "advice_request"
        elif any(word in text_lower for word in ["symptôme", "douleur", "problème", "mal"]):
            return "symptom_report" 
        elif any(word in text_lower for word in ["question", "pourquoi", "comment"]):
            return "information_request"
        else:
            return "general_message"
