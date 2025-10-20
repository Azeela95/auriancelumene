# app/api/routes/voice_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.voice_service import VoiceService

router = APIRouter(prefix="/voice", tags=["Voice"])

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcription audio avec analyse intelligente
    """
    print(f"📥 Réception fichier: {file.filename} ({file.content_type})")
    
    # Vérification du type de fichier
    allowed_types = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/x-wav', 'audio/webm']
    if not file.content_type or file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Type de fichier non supporté. Types autorisés: {allowed_types}"
        )
    
    try:
        service = VoiceService()
        result = await service.transcribe_audio(file)
        
        return {
            "status": "success",
            "transcription": result["text"],
            "detected_language": result["language"],
            "confidence": result["confidence"],
            "analysis": result["analysis"],
            "intent": result["intent"],
            "message": "Transcription et analyse réussies"
        }
    except Exception as e:
        print(f"❌ Erreur API vocale: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la transcription: {str(e)}"
        )

@router.get("/languages")
async def get_supported_languages():
    return {
        "supported_languages": [
            {"code": "fr", "name": "French"},
            {"code": "en", "name": "English"}, 
            {"code": "es", "name": "Spanish"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ar", "name": "Arabic"},
            {"code": "hi", "name": "Hindi"}
        ],
        "total_languages": 99,
        "message": "Whisper supporte 99 langues"
    }

@router.get("/health")
async def voice_health_check():
    return {
        "status": "healthy",
        "service": "Voice Transcription & Analysis",
        "model": "whisper-base",
        "capabilities": ["transcription", "intent_detection", "content_analysis"]
    }