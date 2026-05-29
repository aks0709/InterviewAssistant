"""FastAPI application entry point."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import agent1, agent2, agent3, health

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Interview Assistant API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS origins: {settings.CORS_ORIGINS}")
logger.info(f"Google API Key configured: {'Yes' if settings.GOOGLE_API_KEY != 'placeholder_key' else 'No'}")

# Routes
app.include_router(agent1.router, prefix="/agent1", tags=["Agent1: Similarity"])
app.include_router(agent2.router, prefix="/agent2", tags=["Agent2: Scheduling"])
app.include_router(agent3.router, prefix="/agent3", tags=["Agent3: Questions"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Interview Assistant API"}
