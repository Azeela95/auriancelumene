# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------
# 🔧 Configuration de la base
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./aurian.db"  # tu peux changer par PostgreSQL ou MySQL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# -----------------------------
# 📦 Fonction get_db pour les routes
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
