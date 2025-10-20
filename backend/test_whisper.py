# test_whisper.py
import whisper
import sys

print("🔧 Test d'installation Whisper...")

try:
    # Charge un petit modèle pour tester
    model = whisper.load_model("base")
    print("✅ Whisper installé avec succès !")
    print(f"📊 Modèle chargé: base")
    
    # Test avec un fichier audio si tu en as un
    # Sinon, juste l'import suffit
    print("🎤 Prêt pour la transcription audio !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("💡 Essaye: pip install openai-whisper")