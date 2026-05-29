# Agent 2: Interview Scheduling System

## Overview
Agent 2 handles interview scheduling for shortlisted candidates by automatically assigning available interview panels.

## Features
- **Deterministic Panel Assignment**: No LLM, pure logic-based scheduling
- **Smart Availability**: Prefers free panels, then earliest available
- **Database Integration**: PostgreSQL with proper schema
- **Status Management**: Tracks candidate progression (pending → shortlisted → scheduled)

## Database Schema

### Tables
1. **panels** - Interview panel members
   - id, name, email, expertise, busy_until
2. **candidates** - Candidate information
   - id, name, email, phone, resume_path, similarity_score, status
3. **interviews** - Scheduled interviews
   - id, candidate_id, panel_id, scheduled_time, duration, status

## Setup Instructions

### 1. Install PostgreSQL (if not installed)
```bash
# Windows: Download from postgresql.org
# Or use Docker:
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

### 2. Update Database URL in .env
```
DATABASE_URL=postgresql://user:password@localhost:5432/interview_assistant
```

### 3. Initialize Database
```bash
cd backend
python init_db.py
```

This creates tables and seeds 5 initial panels.

### 4. Add Test Candidates (Optional)
```bash
python add_test_candidates.py
```

## API Endpoints

### Schedule Interview
```http
POST /agent2/schedule
Content-Type: application/json

{
  "candidate_id": 1
}
```

**Response:**
```json
{
  "interview_id": 1,
  "candidate_id": 1,
  "candidate_name": "Alice Johnson",
  "panel_id": 1,
  "panel_name": "John Smith",
  "scheduled_time": "2024-01-15T10:00:00",
  "duration_minutes": 60,
  "status": "scheduled",
  "meeting_link": "https://meet.example.com/1-1",
  "message": "Interview scheduled with John Smith on 2024-01-15 10:00"
}
```

### Get Interview Details
```http
GET /agent2/interview/{interview_id}
```

## Scheduling Logic

### Panel Selection Priority:
1. **Never assigned** (busy_until is NULL)
2. **Currently free** (busy_until < now)
3. **Earliest available** (smallest busy_until)

### Time Calculation:
- If panel free: Schedule in 1 hour
- If panel busy: Schedule 15 minutes after busy_until

### Status Transitions:
```
pending → shortlisted (by Agent 1)
shortlisted → scheduled (by Agent 2)
scheduled → completed (manual/future)
```

## Testing

### Test Scheduling Flow:
```bash
# 1. Start backend
cd backend
start.bat

# 2. Schedule interview for candidate 1
curl -X POST http://localhost:8001/agent2/schedule \
  -H "Content-Type: application/json" \
  -d '{"candidate_id": 1}'

# 3. Get interview details
curl http://localhost:8001/agent2/interview/1
```

## Integration with Agent 1

Agent 1 evaluates candidates and sets status to "shortlisted" if similarity_score >= 80%.
Agent 2 then schedules interviews for all shortlisted candidates.

## Notes

- **No LLM**: Pure deterministic logic for reliability
- **Atomic Operations**: Database transactions ensure consistency
- **Scalable**: Can handle multiple concurrent scheduling requests
- **Zero Impact on Agent 1**: Completely separate service