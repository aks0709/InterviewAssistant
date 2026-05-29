"""SQLAlchemy database setup and models."""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Panel(Base):
    """Interview panel model."""
    __tablename__ = "panels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False)
    expertise = Column(String(255))  # e.g., "Java", "Python", "Frontend"
    busy_until = Column(DateTime, nullable=True)  # NULL = available
    created_at = Column(DateTime, default=datetime.utcnow)

class Candidate(Base):
    """Candidate model."""
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(50))
    resume_path = Column(String(500))
    similarity_score = Column(Integer)  # From Agent 1
    overlapping_skills = Column(Text)  # JSON string of overlapping skills from Agent 1
    status = Column(String(50), default="pending")  # pending, shortlisted, scheduled, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Interview(Base):
    """Interview scheduling model."""
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False)
    candidate_name = Column(String(255), nullable=False)
    candidate_email = Column(String(255), nullable=False)
    panel_id = Column(Integer, nullable=False)
    panel_name = Column(String(255), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    meeting_link = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
