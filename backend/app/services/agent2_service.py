"""Agent 2 Service: Interview Scheduling with Panel Assignment."""
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from sqlalchemy.orm import Session
from app.models.database import Panel, Candidate, Interview

logger = logging.getLogger(__name__)

class Agent2Service:
    """Service for scheduling interviews with panel assignment."""
    
    def __init__(self):
        """Initialize Agent 2 service."""
        logger.info("Agent2Service initialized")
    
    def schedule_interview(self, candidate_id: int, db: Session) -> Dict:
        """
        Auto-schedule interview for shortlisted candidate with Indian timezone.
        
        Logic:
        1. Check if candidate already has interview -> return existing (same panel)
        2. Find available panel (round-robin assignment)
        3. Schedule at panel's next available slot (busy_until + 1 hour)
        4. If panel free, schedule in 1 hour from now (IST)
        5. Update panel busy_until to scheduled_time + 1 hour
        """
        try:
            # Indian timezone (UTC+5:30)
            IST = timezone(timedelta(hours=5, minutes=30))
            now_ist = datetime.now(IST)
            
            logger.info(f"Scheduling for candidate_id: {candidate_id} at {now_ist}")
            
            # 1. Get candidate
            candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
            if not candidate:
                raise ValueError(f"Candidate {candidate_id} not found")
            
            if candidate.status not in ["shortlisted", "scheduled"]:
                raise ValueError(f"Candidate not shortlisted (status: {candidate.status})")
            
            # 2. Check existing interview
            existing = db.query(Interview).filter(
                Interview.candidate_id == candidate_id,
                Interview.status == "scheduled"
            ).first()
            
            if existing:
                logger.info(f"Returning existing interview with {existing.panel_name}")
                return {
                    "interview_id": existing.id,
                    "candidate_id": candidate.id,
                    "candidate_name": candidate.name,
                    "panel_id": existing.panel_id,
                    "panel_name": existing.panel_name,
                    "scheduled_time": existing.scheduled_time.isoformat(),
                    "duration_minutes": 60,
                    "status": "scheduled",
                    "meeting_link": existing.meeting_link,
                    "message": f"Interview already scheduled with {existing.panel_name}"
                }
            
            # 3. Find available panel
            panel = self._find_available_panel(db)
            if not panel:
                raise ValueError("No panels available")
            
            # 4. Calculate scheduled time
            if panel.busy_until is None:
                scheduled_time = now_ist + timedelta(hours=1)
            else:
                panel_busy_ist = panel.busy_until.replace(tzinfo=IST)
                scheduled_time = panel_busy_ist + timedelta(hours=1)
            
            # 5. Create interview
            interview = Interview(
                candidate_id=candidate.id,
                candidate_name=candidate.name,
                candidate_email=candidate.email,
                panel_id=panel.id,
                panel_name=panel.name,
                scheduled_time=scheduled_time.replace(tzinfo=None),
                duration_minutes=60,
                status="scheduled",
                meeting_link=f"https://meet.example.com/{candidate.id}-{panel.id}",
                notes=f"Auto-scheduled interview"
            )
            db.add(interview)
            
            # 6. Update panel busy_until
            panel.busy_until = scheduled_time.replace(tzinfo=None)
            
            # 7. Update candidate status
            candidate.status = "scheduled"
            candidate.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(interview)
            
            logger.info(f"Interview scheduled: {interview.id} with {panel.name} at {scheduled_time}")
            
            return {
                "interview_id": interview.id,
                "candidate_id": candidate.id,
                "candidate_name": candidate.name,
                "panel_id": panel.id,
                "panel_name": panel.name,
                "scheduled_time": scheduled_time.isoformat(),
                "duration_minutes": 60,
                "status": "scheduled",
                "meeting_link": interview.meeting_link,
                "message": f"Interview scheduled with {panel.name} at {scheduled_time.strftime('%Y-%m-%d %H:%M IST')}"
            }
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error scheduling: {str(e)}", exc_info=True)
            raise
    
    def _find_available_panel(self, db: Session) -> Optional[Panel]:
        """
        Find available panel using round-robin logic.
        Priority: NULL busy_until -> earliest busy_until
        """
        # Priority 1: Never assigned (busy_until is NULL)
        panel = db.query(Panel).filter(Panel.busy_until.is_(None)).first()
        if panel:
            return panel
        
        # Priority 2: Panel with earliest busy_until (round-robin)
        panel = db.query(Panel).order_by(Panel.busy_until.asc()).first()
        return panel
    
    def get_interview(self, interview_id: int, db: Session) -> Dict:
        """Get interview details by ID."""
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise ValueError(f"Interview {interview_id} not found")
        
        return {
            "interview_id": interview.id,
            "candidate_id": interview.candidate_id,
            "candidate_name": interview.candidate_name,
            "panel_name": interview.panel_name,
            "scheduled_time": interview.scheduled_time.isoformat(),
            "duration_minutes": interview.duration_minutes,
            "status": interview.status,
            "meeting_link": interview.meeting_link
        }
