"""Application configuration from environment variables."""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from .env file."""
    
    # Google AI
    GOOGLE_API_KEY: str = "placeholder_key"
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/interview_assistant"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
