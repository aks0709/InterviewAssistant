"""Agent 1 API routes: /agent1/evaluate"""
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services.agent1.agent1_service import Agent1Service
from app.services.file_parser import parse_file
from app.models.database import get_db, Candidate
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()
agent1_service = Agent1Service()

@router.post("/evaluate")
async def evaluate_similarity(jd_file: UploadFile = File(...), resume_file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Evaluate JD-Resume similarity using uploaded files.
    
    Endpoint: POST /agent1/evaluate
    Files: jd_file, resume_file (PDF, DOCX, TXT)
    """
    try:
        # Read and parse JD file
        jd_content = await jd_file.read()
        jd_text = parse_file(jd_content, jd_file.filename)
        logger.info(f"JD file parsed: {jd_file.filename}, length: {len(jd_text)}")
        
        # Read and parse Resume file
        resume_content = await resume_file.read()
        resume_text = parse_file(resume_content, resume_file.filename)
        logger.info(f"Resume file parsed: {resume_file.filename}, length: {len(resume_text)}")
        
        # Evaluate similarity
        result = agent1_service.evaluate_similarity(
            jd_text=jd_text,
            resume_text=resume_text
        )
        
        # Extract candidate name and email from resume
        candidate_name = _extract_name_from_filename(resume_file.filename)
        candidate_email = _extract_email_from_resume(resume_text)
        
        # Create or update candidate in database
        candidate = db.query(Candidate).filter(Candidate.email == candidate_email).first()
        
        # Store overlapping skills as JSON string
        import json
        overlapping_skills_json = json.dumps(result.get('matched_skills', []))
        
        if not candidate:
            # Create new candidate
            candidate = Candidate(
                name=candidate_name,
                email=candidate_email,
                phone="",
                resume_path=resume_file.filename,
                similarity_score=int(result['match_percentage']),
                overlapping_skills=overlapping_skills_json,
                status="shortlisted" if result['match_percentage'] >= 70 else "pending"
            )
            db.add(candidate)
        else:
            # Update existing candidate
            candidate.similarity_score = int(result['match_percentage'])
            candidate.overlapping_skills = overlapping_skills_json
            candidate.status = "shortlisted" if result['match_percentage'] >= 70 else "pending"
            candidate.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(candidate)
        
        # Add candidate info to result
        result['candidate_id'] = candidate.id
        result['candidate_name'] = candidate.name
        result['candidate_email'] = candidate.email
        result['status'] = candidate.status
        
        logger.info(f"Evaluation completed - Score: {result.get('similarity_score', 'N/A')}, Candidate ID: {candidate.id}")
        return result
        
    except Exception as e:
        logger.error(f"Error evaluating similarity: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error evaluating similarity: {str(e)}")

def _extract_name_from_filename(filename: str) -> str:
    """Extract candidate name from filename (e.g., AyushKumar.txt -> Ayush Kumar)."""
    import re
    import os
    
    # Remove file extension
    name = os.path.splitext(filename)[0]
    
    # Remove common prefixes/suffixes
    name = re.sub(r'(?i)(resume|cv|_resume|_cv|-resume|-cv)', '', name)
    
    # Split camelCase or PascalCase (e.g., AyushKumar -> Ayush Kumar)
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    
    # Replace underscores and hyphens with spaces
    name = name.replace('_', ' ').replace('-', ' ')
    
    # Clean up extra spaces
    name = ' '.join(name.split())
    
    # Capitalize each word
    name = name.title()
    
    # Validate
    if name and 2 <= len(name) <= 100:
        return name
    
    return "Unknown Candidate"

def _extract_name_from_resume(text: str) -> str:
    """Extract candidate name from resume text using improved heuristics."""
    import re
    
    # Try to find name after "Name:" or similar labels
    name_patterns = [
        r'(?:Name|NAME|Full Name|Candidate Name)\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',  # First line with capitalized words
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            name = match.group(1).strip()
            # Validate: name should be 2-50 chars, not look like a filename
            if 2 <= len(name) <= 50 and not any(ext in name.lower() for ext in ['.pdf', '.doc', '.txt', 'resume', 'cv']):
                return name
    
    # Fallback: get first line but validate it's not a filename
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if lines:
        first_line = lines[0][:100]
        # Check if it looks like a name (has spaces, capitalized, no file extensions)
        if ' ' in first_line and not any(ext in first_line.lower() for ext in ['.pdf', '.doc', '.txt', 'resume', 'cv', 'jd']):
            return first_line
    
    return "Unknown Candidate"

def _extract_email_from_resume(text: str) -> str:
    """Extract email from resume text."""
    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    if matches:
        return matches[0]
    # Generate a unique email if not found
    import uuid
    return f"candidate_{uuid.uuid4().hex[:8]}@temp.com"