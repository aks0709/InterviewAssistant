"""Gemini LLM service using gemini-2.5-flash."""
import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

LLM_MODEL = "gemini-2.5-flash"

def generate_response(prompt: str):
    """Generate response using Gemini 2.5 Flash."""
    pass

def generate_with_context(prompt: str, context: str):
    """Generate response with conversation context."""
    pass
