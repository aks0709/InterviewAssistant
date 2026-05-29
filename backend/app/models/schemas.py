"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Agent 1: Similarity
class EvaluateRequest(BaseModel):
    """Request schema for JD-Resume similarity evaluation."""
    jd_text: str
    resume_text: str

class EvaluateResponse(BaseModel):
    """Response schema for similarity evaluation."""
    similarity_score: float
    match_percentage: float
    key_matches: List[str]
    missing_skills: List[str]
    recommendations: str

# Agent 2: Scheduling
class ScheduleRequest(BaseModel):
    """Request schema for interview scheduling."""
    candidate_name: str
    candidate_email: str
    interviewer_name: str
    interviewer_email: str
    scheduled_time: datetime
    duration_minutes: Optional[int] = 60
    meeting_link: Optional[str] = None
    notes: Optional[str] = None

class ScheduleResponse(BaseModel):
    """Response schema for scheduling."""
    interview_id: int
    status: str
    message: str
    scheduled_time: datetime
    meeting_details: dict

# Agent 3: Questions
class QuestionsRequest(BaseModel):
    """Request schema for interview question generation."""
    jd_text: str
    resume_text: str
    difficulty_level: str = "medium"  # easy, medium, hard
    question_count: Optional[int] = 10
    focus_areas: Optional[List[str]] = None

class QuestionsResponse(BaseModel):
    """Response schema for generated questions."""
    questions: List[dict]
    total_count: int
    difficulty_level: str
    estimated_duration: int

class FollowupRequest(BaseModel):
    """Request schema for follow-up questions."""
    previous_qa: List[dict]
    context: str
    question_count: Optional[int] = 3

class FollowupResponse(BaseModel):
    """Response schema for follow-up questions."""
    followup_questions: List[str]
    reasoning: str
