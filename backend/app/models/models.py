# backend/app/models/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

# ----------------------
# USERS
# ----------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    language = Column(String, default="fr")      # FR/EN/ZH
    timezone = Column(String, default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    consents = relationship("Consent", back_populates="user")
    habits = relationship("Habit", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    suggestions = relationship("Suggestion", back_populates="user")


# ----------------------
# CONSENTS
# ----------------------
class Consent(Base):
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    consent_type = Column(String, nullable=False)   # ex: "general", "camera"
    given = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="consents")


# ----------------------
# HABITS
# ----------------------
class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    habit_type = Column(String, nullable=False)    # repas, sommeil, activité, hydratation, humeur
    value = Column(String, nullable=False)         # ex: "30 min", "2L", "happy"
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="habits")


# ----------------------
# MEASUREMENTS
# ----------------------
class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    measure_type = Column(String, nullable=False)  # ex: "weight", "blood_pressure"
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)           # ex: "kg", "mmHg"
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


# ----------------------
# CHAT SESSIONS & MESSAGES
# ----------------------
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False)         # "user" / "bot"
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


# ----------------------
# SUGGESTIONS
# ----------------------
class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    habit_type = Column(String, nullable=False)
    suggestion_text = Column(String, nullable=False)
    source_id = Column(Integer, ForeignKey("content_sources.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="suggestions")
    source = relationship("ContentSource", back_populates="suggestions")


# ----------------------
# CONTENT SOURCES
# ----------------------
class ContentSource(Base):
    __tablename__ = "content_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)       # ex: "WHO Guidelines"
    url = Column(String, nullable=True)         # lien vers la source
    last_verified = Column(DateTime)

    suggestions = relationship("Suggestion", back_populates="source")


# ----------------------
# SEEDS MINIMALES (OPTIONNEL)
# ----------------------
def create_initial_seeds(session):
    from app.models.models import ContentSource, User, Consent

    # Content sources
    sources = [
        ContentSource(name="WHO Guidelines", url="https://www.who.int"),
        ContentSource(name="Public Health France", url="https://www.santepubliquefrance.fr")
    ]
    session.add_all(sources)

    # Test user
    user = User(email="test@example.com", hashed_password="hashed_password_test")
    session.add(user)
    session.commit()

    # Consent example
    consent = Consent(user_id=user.id, consent_type="general", given=True)
    session.add(consent)
    session.commit()
