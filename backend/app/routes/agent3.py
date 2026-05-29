"""Agent 3 API routes: /agent3/questions"""
import logging
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.services.agent3.agent3_service import Agent3Service
from app.models.database import get_db, Candidate

logger = logging.getLogger(__name__)
router = APIRouter()
agent3_service = Agent3Service()

class QuestionRequest(BaseModel):
    candidate_id: int
    custom_requirements: Optional[str] = None

@router.post("/questions")
async def generate_questions(request: QuestionRequest, db: Session = Depends(get_db)):
    """
    Generate interview questions based on candidate's overlapping skills.
    
    Endpoint: POST /agent3/questions
    Body: {
        "candidate_id": 123,
        "custom_requirements": "Focus on React hooks and state management" (optional)
    }
    """
    try:
        candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
        
        if not candidate:
            raise HTTPException(status_code=404, detail=f"Candidate with ID {request.candidate_id} not found")
        
        if not candidate.similarity_score:
            raise HTTPException(
                status_code=400, 
                detail="Candidate has not been evaluated yet. Please run Agent 1 first."
            )
        
        # Get overlapping skills from candidate record
        overlapping_skills = []
        if candidate.overlapping_skills:
            try:
                overlapping_skills = json.loads(candidate.overlapping_skills)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse overlapping_skills for candidate {candidate.id}")
        
        if not overlapping_skills:
            raise HTTPException(
                status_code=400,
                detail="No overlapping skills found for this candidate. Cannot generate questions."
            )
        
        # Generate questions
        result = agent3_service.generate_questions(
            overlapping_skills=overlapping_skills,
            custom_requirements=request.custom_requirements
        )
        
        # Add candidate info to response
        result['candidate_id'] = candidate.id
        result['candidate_name'] = candidate.name
        result['candidate_email'] = candidate.email
        
        logger.info(f"Questions generated for candidate {candidate.id} ({candidate.name})")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")
