"""Pydantic schemas for Agent 1."""
from pydantic import BaseModel
from typing import List, Dict

class EvaluateRequest(BaseModel):
    """Request schema for JD-Resume evaluation."""
    jd_text: str
    resume_text: str

class MatchedTopic(BaseModel):
    """Matched topic between JD and Resume."""
    resume_snippet: str
    jd_match: str
    score: float

class EvaluateResponse(BaseModel):
    """Response schema for similarity evaluation."""
    similarity_score: float
    matched_topics: List[Dict]
    decision: str
    threshold: float
