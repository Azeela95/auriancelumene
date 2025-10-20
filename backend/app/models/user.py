from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    role = Column(String, default="patient")
    language = Column(String, default="fr")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # GARDE SEULEMENT les relationships ESSENTIELLES pour commencer
    # habitudes = relationship("Habitude", back_populates="user")
    # resources = relationship("UserResource", back_populates="user")
    # queries = relationship("Query", back_populates="user")
    # recommendations = relationship("Recommendation", back_populates="user")
    
    # COMMENCE PAR COMMENTER TOUTES les relationships :
    # habitudes = relationship("Habitude", back_populates="user")
    # resources = relationship("UserResource", back_populates="user")
    # queries = relationship("Query", back_populates="user")
    # recommendations = relationship("Recommendation", back_populates="user")
    # rdvs = relationship("RDV", back_populates="infermier")
    # notifications = relationship("Notification", back_populates="user")
    # audit_logs = relationship("AuditLog", back_populates="user")
    # consents = relationship("Consent", back_populates="user")  # ⬅️ CELUI-CI CAUSE L'ERREUR
    # patients = relationship("Patient", back_populates="user")
    # plannings = relationship("Planning", back_populates="user")