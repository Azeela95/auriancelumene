# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import des routes internes
from app.api.routes import (
    user_routes,
    habitude_routes,
    patient_routes,
    planning_routes,
    notification_routes,
    health_routes,
    ai_routes,
    voice_routes,
    agent_routes,
    knowledge_routes,
    # 🆕 NOUVELLES APIS
    camera_routes,
    prediction_routes,
    gamification_routes,
    social_routes
)

app = FastAPI(
    title="AurianCelumene API",
    version="0.1.0",
    description="Backend principal pour la plateforme AurianCelumene 🌿"
)

# --- Middleware CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Enregistrement des routes principales ---
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(habitude_routes.router, prefix="/habitudes", tags=["Habitudes"])
app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])
app.include_router(planning_routes.router, prefix="/plannings", tags=["Plannings"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["Notifications"])
app.include_router(health_routes.router, prefix="/health", tags=["Health"])
app.include_router(ai_routes.router, prefix="/ai", tags=["AI"])
app.include_router(voice_routes.router, prefix="/voice", tags=["Voice"])
app.include_router(agent_routes.router, prefix="/agents", tags=["Agents"])
app.include_router(knowledge_routes.router, prefix="/knowledge", tags=["Knowledge"])

# 🆕 NOUVELLES APIS RÉVOLUTIONNAIRES
app.include_router(camera_routes.router, prefix="/camera", tags=["Camera Analysis"])
app.include_router(prediction_routes.router, prefix="/predictions", tags=["Health Predictions"])
app.include_router(gamification_routes.router, prefix="/gamification", tags=["Health Gamification"])
app.include_router(social_routes.router, prefix="/social", tags=["Health Social Network"])

# --- Route racine ---
@app.get("/")
def root():
    return {"message": "AurianCelumene backend running 🚀"}