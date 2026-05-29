"""Health check routes for monitoring system status."""
import logging
from fastapi import APIRouter
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/llm")
def health_llm():
    """
    Health check for LLM configuration.
    
    Returns:
        - Agent 1: Uses google-generativeai (legacy) for embeddings
        - Agent 3: Uses google-genai (v1) for text generation with gemini-2.5-flash
    """
    return {
        "status": "ok",
        "agent1_embeddings": {
            "sdk": "google-generativeai",
            "model": "models/gemini-embedding-001"
        },
        "agent3_text_generation": {
            "sdk": "google-genai",
            "model": "gemini-2.5-flash"
        },
        "api_key_configured": bool(settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "placeholder_key")
    }
