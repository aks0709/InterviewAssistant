"""Agent 2 API routes: /agent2/schedule"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.database import get_db
from app.services.agent2_service import Agent2Service

logger = logging.getLogger(__name__)
router = APIRouter()
agent2_service = Agent2Service()

class ScheduleRequest(BaseModel):
    """Request schema for scheduling interview."""
    candidate_id: int

class ScheduleResponse(BaseModel):
    """Response schema for scheduled interview."""
    interview_id: int
    candidate_id: int
    candidate_name: str
    panel_id: int
    panel_name: str
    scheduled_time: str
    duration_minutes: int
    status: str
    meeting_link: str
    message: str

@router.post("/schedule", response_model=ScheduleResponse)
async def schedule_interview(request: ScheduleRequest, db: Session = Depends(get_db)):
    """
    Auto-schedule interview for shortlisted candidate.
    
    Endpoint: POST /agent2/schedule
    Body: {"candidate_id": 1}
    """
    try:
        logger.info(f"Received scheduling request for candidate_id: {request.candidate_id}")
        
        result = agent2_service.schedule_interview(
            candidate_id=request.candidate_id,
            db=db
        )
        
        logger.info(f"Interview scheduled successfully: {result['interview_id']}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error scheduling interview: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error scheduling interview: {str(e)}")

@router.get("/interview/{interview_id}")
async def get_interview(interview_id: int, db: Session = Depends(get_db)):
    """
    Get interview details by ID.
    
    Endpoint: GET /agent2/interview/{interview_id}
    """
    try:
        result = agent2_service.get_interview(interview_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
