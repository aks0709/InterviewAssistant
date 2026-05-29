"""Gemini embeddings service."""
import logging
from typing import List
from app.config import settings

logger = logging.getLogger(__name__)

def get_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text using Gemini embedding-001.
    
    Args:
        text: Input text
    
    Returns:
        Embedding vector as list of floats
    """
    try:
        import google.generativeai as genai
        
        # Configure Gemini API
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        logger.debug(f"Generating embedding for text of length: {len(text)}")
        result = genai.embed_content(
            model=settings.EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        logger.debug(f"Embedding generated successfully, dimension: {len(result['embedding'])}")
        return result['embedding']
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        raise

def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    
    Args:
        texts: List of input texts
    
    Returns:
        List of embedding vectors
    """
    logger.info(f"Generating embeddings for {len(texts)} texts")
    embeddings = []
    for i, text in enumerate(texts):
        try:
            embedding = get_embedding(text)
            embeddings.append(embedding)
            logger.debug(f"Generated embedding {i+1}/{len(texts)}")
        except Exception as e:
            logger.error(f"Failed to generate embedding for text {i+1}: {str(e)}")
            raise
    logger.info(f"Successfully generated {len(embeddings)} embeddings")
    return embeddings
