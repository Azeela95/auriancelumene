from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User
from app.models.consent import Consent

# Connexion PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:110603@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

# Exemple simple pour tester
new_user = User(email="test@example.com", hashed_password="password")
db.add(new_user)

try:
    db.commit()
    print(f"Utilisateur ajouté avec ID: {new_user.id}")
except Exception as e:
    db.rollback()
    print("Erreur:", e)
finally:
    db.close()
