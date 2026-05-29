"""Gemini embeddings service using google-generativeai SDK."""
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

EMBEDDING_MODEL = "models/embedding-001"

def get_embeddings(text: str):
    """Generate embeddings using Gemini embedding-001 model."""
    pass

def get_batch_embeddings(texts: list):
    """Generate embeddings for multiple texts."""
    pass
