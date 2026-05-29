"""
Conversation History Storage Structure

Location: backend/data/history/

Structure:
- Each evaluation creates a timestamped JSON file
- File naming: {timestamp}_{decision}.json

Example file: 2024-01-15_143022_shortlisted.json
{
    "timestamp": "2024-01-15T14:30:22",
    "jd_text": "...",
    "resume_text": "...",
    "similarity_score": 0.85,
    "matched_topics": [...],
    "decision": "shortlisted"
}

Usage:
- History files can be loaded for analytics
- Used for tracking evaluation patterns
- Can be queried for candidate re-evaluation

Note: This is a simple file-based approach.
For production, consider using a proper database.
"""
