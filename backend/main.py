from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import user_routes, habitude_routes  # ajoute tes routes habitude ici

app = FastAPI(title="AurianCelumene API", version="0.1.0")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(habitude_routes.router, prefix="/habitudes", tags=["Habitudes"])

@app.get("/")
def root():
    return {"message": "AurianCelumene backend running 🚀"}
