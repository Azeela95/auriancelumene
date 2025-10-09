from fastapi import FastAPI
from app.api.routes.user_routes import router as user_router

app = FastAPI(title="Auriance Lumene API", version="1.0")

app.include_router(user_router, prefix="/api/users", tags=["users"])

@app.get("/")
def root():
    return {"message": "Auriance Lumene API Running!"}

