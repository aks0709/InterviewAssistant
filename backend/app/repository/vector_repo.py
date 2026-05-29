"""Improved vector repository with proper scoping and cosine similarity."""
import pickle
import math
import uuid
from typing import List, Tuple, Dict, Optional
from pathlib import Path

VECTOR_DIR = Path(__file__).parent.parent.parent.parent / "data" / "vectors"
VECTORS_FILE = VECTOR_DIR / "vectors.pkl"

class VectorRepository:
    """Improved vector store with metadata scoping."""
    
    def __init__(self):
        """Initialize vector store."""
        self.vectors = []
        self.metadata = []
        self.session_id = str(uuid.uuid4())
        VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    
    def add_vectors(self, embeddings: List[List[float]], texts: List[str], doc_type: str):
        """Add vectors with proper metadata scoping."""
        for embedding, text in zip(embeddings, texts):
            # Skip boilerplate chunks
            if len(text.strip()) < 20 or self._is_generic_text(text):
                continue
                
            self.vectors.append(embedding)
            self.metadata.append({
                "text": text,
                "doc_type": doc_type,
                "session_id": self.session_id,
                "doc_id": f"{doc_type}_{self.session_id}"
            })
    
    def _is_generic_text(self, text: str) -> bool:
        """Check if text is too generic/boilerplate."""
        generic_terms = ["experience", "skills", "responsibilities", "requirements", 
                        "qualifications", "education", "background", "summary"]
        text_lower = text.lower()
        return len([term for term in generic_terms if term in text_lower]) > 2
    
    def search_scoped(self, query_embedding: List[float], target_doc_type: str, k: int = 5) -> List[Tuple[float, str]]:
        """Search with proper scoping to prevent cross-contamination."""
        if not self.vectors:
            return []
        
        similarities = []
        for i, vector in enumerate(self.vectors):
            metadata = self.metadata[i]
            
            # Only search within current session and target doc type
            if (metadata["session_id"] == self.session_id and 
                metadata["doc_type"] == target_doc_type):
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(query_embedding, vector)
                similarities.append((similarity, metadata["text"]))
        
        # Sort by similarity (descending) and return top k
        similarities.sort(key=lambda x: x[0], reverse=True)
        return similarities[:k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)
    
    def get_scope_counts(self) -> Dict[str, int]:
        """Get document counts by type for current session."""
        counts = {}
        for metadata in self.metadata:
            if metadata["session_id"] == self.session_id:
                doc_type = metadata["doc_type"]
                counts[doc_type] = counts.get(doc_type, 0) + 1
        return counts
    
    def save(self):
        """Save vectors to disk."""
        data = {"vectors": self.vectors, "metadata": self.metadata}
        with open(VECTORS_FILE, 'wb') as f:
            pickle.dump(data, f)
    
    def clear(self):
        """Clear vectors and metadata for new session."""
        self.vectors = []
        self.metadata = []
        self.session_id = str(uuid.uuid4())