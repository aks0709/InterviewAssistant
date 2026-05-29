"""Improved Agent 1 Service with proper similarity scoring."""
import logging
import math
from typing import Dict, List
from app.utils.chunks import chunk_text
from app.services.agent1.embeddings_service import get_batch_embeddings
from app.repository.vector_repo import VectorRepository
from app.services.skills_extractor import SkillsExtractor

logger = logging.getLogger(__name__)

class Agent1Service:
    """Improved service for JD-Resume similarity evaluation."""
    
    def __init__(self):
        """Initialize Agent 1 service."""
        self.vector_repo = VectorRepository()
        self.skills_extractor = SkillsExtractor()
        logger.info("Agent1Service initialized with improved scoring")
    
    def evaluate_similarity(self, jd_text: str, resume_text: str) -> Dict:
        """
        Evaluate similarity with improved algorithm.
        
        Returns comprehensive similarity analysis with semantic and skills components.
        """
        try:
            logger.info("Starting improved similarity evaluation")
            
            # Clear previous data
            self.vector_repo.clear()
            
            # Chunk documents
            jd_chunks = chunk_text(jd_text, chunk_size=500, overlap=50)
            resume_chunks = chunk_text(resume_text, chunk_size=500, overlap=50)
            logger.info(f"Text chunked - JD: {len(jd_chunks)}, Resume: {len(resume_chunks)}")
            
            if not jd_chunks or not resume_chunks:
                return self._empty_result("Empty or invalid documents")
            
            # Generate embeddings
            jd_embeddings = get_batch_embeddings(jd_chunks)
            resume_embeddings = get_batch_embeddings(resume_chunks)
            logger.info(f"Embeddings generated - JD: {len(jd_embeddings)}, Resume: {len(resume_embeddings)}")
            
            # Store embeddings with proper scoping
            self.vector_repo.add_vectors(jd_embeddings, jd_chunks, "jd")
            self.vector_repo.add_vectors(resume_embeddings, resume_chunks, "resume")
            
            # Verify scope counts
            scope_counts = self.vector_repo.get_scope_counts()
            logger.info(f"Scope counts: {scope_counts}")
            
            # Calculate semantic similarity (bidirectional)
            semantic_score = self._calculate_semantic_similarity(jd_embeddings, resume_embeddings)
            logger.info(f"Semantic similarity: {semantic_score:.4f}")
            
            # Extract skills from both documents
            jd_skills = self.skills_extractor.extract_skills(jd_text, is_jd=True)
            resume_skills = self.skills_extractor.extract_skills(resume_text, is_jd=False)
            
            # Calculate skills overlap
            skills_analysis = self.skills_extractor.calculate_skills_overlap(jd_skills, resume_skills)
            skills_overlap = skills_analysis["skills_overlap"]
            logger.info(f"Skills overlap: {skills_overlap:.4f}")
            
            # Calculate final score with penalties
            final_score = self._calculate_final_score(semantic_score, skills_overlap, skills_analysis)
            
            # Generate top snippets for display
            top_snippets = self._get_top_snippets(resume_embeddings, resume_chunks)
            
            result = {
                "similarity_score": round(final_score, 4),
                "match_percentage": round(final_score * 100, 2),
                "semantic": round(semantic_score, 4),
                "skills_overlap": round(skills_overlap, 4),
                "key_matches": skills_analysis["matched_required"] + skills_analysis["matched_preferred"][:3],
                "missing_skills": skills_analysis["missing_required"][:5],
                "matched_skills": skills_analysis["matched_required"] + skills_analysis["matched_preferred"],
                "missing_required": skills_analysis["missing_required"],
                "top_snippets": top_snippets,
                "recommendations": self._generate_recommendations(final_score, skills_analysis)
            }
            
            logger.info(f"Final evaluation - Score: {final_score:.4f}")
            return result
            
        except Exception as e:
            logger.error(f"Error in evaluate_similarity: {str(e)}", exc_info=True)
            raise
    
    def _calculate_semantic_similarity(self, jd_embeddings: List, resume_embeddings: List) -> float:
        """Calculate symmetric semantic similarity."""
        # JD -> Resume similarity
        jd_to_resume_scores = []
        for jd_emb in jd_embeddings:
            results = self.vector_repo.search_scoped(jd_emb, "resume", k=3)
            if results:
                avg_sim = sum(sim for sim, _ in results) / len(results)
                jd_to_resume_scores.append(avg_sim)
        
        # Resume -> JD similarity  
        resume_to_jd_scores = []
        for resume_emb in resume_embeddings:
            results = self.vector_repo.search_scoped(resume_emb, "jd", k=3)
            if results:
                avg_sim = sum(sim for sim, _ in results) / len(results)
                resume_to_jd_scores.append(avg_sim)
        
        # Symmetric average
        jd_to_resume_avg = sum(jd_to_resume_scores) / len(jd_to_resume_scores) if jd_to_resume_scores else 0.0
        resume_to_jd_avg = sum(resume_to_jd_scores) / len(resume_to_jd_scores) if resume_to_jd_scores else 0.0
        
        return (jd_to_resume_avg + resume_to_jd_avg) / 2.0
    
    def _calculate_final_score(self, semantic: float, skills_overlap: float, skills_analysis: Dict) -> float:
        """Calculate final score with penalties."""
        # Base weighted score
        base_score = 0.60 * semantic + 0.40 * skills_overlap
        
        # Penalty for missing required skills
        total_required = skills_analysis["total_required"]
        missing_required = len(skills_analysis["missing_required"])
        pen_req = 0.15 * (missing_required / max(1, total_required))
        
        # Penalty for off-topic (high semantic but low skills overlap)
        pen_offtopic = 0.10 if semantic >= 0.75 and skills_overlap < 0.2 else 0.0
        
        # Final score with penalties
        final_score = base_score - pen_req - pen_offtopic
        
        return max(0.0, min(1.0, final_score))
    
    def _get_top_snippets(self, resume_embeddings: List, resume_chunks: List) -> List[str]:
        """Get top matching snippets for display."""
        snippets = []
        for resume_emb, resume_chunk in zip(resume_embeddings[:5], resume_chunks[:5]):
            results = self.vector_repo.search_scoped(resume_emb, "jd", k=1)
            if results and results[0][0] > 0.6:  # High similarity threshold
                snippets.append(resume_chunk[:100])
        return snippets[:3]
    
    def _generate_recommendations(self, score: float, skills_analysis: Dict) -> str:
        """Generate recommendations based on comprehensive analysis."""
        if score >= 0.80:
            return "Excellent match. Strong alignment in both technical skills and experience."
        elif score >= 0.70:
            return f"Good match. Consider for interview. Focus on {len(skills_analysis['missing_required'])} missing required skills."
        elif score >= 0.50:
            return "Moderate match. Significant skill gaps need assessment during interview."
        else:
            return "Poor match. Major misalignment in required technical skills."
    
    def _empty_result(self, message: str) -> Dict:
        """Return empty result structure."""
        return {
            "similarity_score": 0.0,
            "match_percentage": 0.0,
            "semantic": 0.0,
            "skills_overlap": 0.0,
            "key_matches": [],
            "missing_skills": [],
            "matched_skills": [],
            "missing_required": [],
            "top_snippets": [],
            "recommendations": message
        }