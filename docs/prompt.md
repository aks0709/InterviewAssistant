# Interview Assistant - Prompt History

## Project Overview
AI-powered Interview Assistant with two main agents:
1. **Agent 1**: JD-Resume Similarity Analysis using Gemini embeddings and LLM-based skills extraction
2. **Agent 2**: Interview Scheduling with PostgreSQL database and deterministic panel assignment

---

## Agent 1: Similarity Analysis Prompts

### Initial Implementation Request
```
Build Agent 1 for JD-Resume similarity analysis:
- Use Gemini embeddings for semantic similarity
- Implement FAISS-like vector similarity
- Extract skills from JD and Resume using LLM
- Calculate match percentage with weighted scoring
- Support PDF and TXT file uploads
```

### Skills Extraction Enhancement
```
Improve skills extraction:
- Use LLM (Gemini) to extract skills from text
- Implement atomic skill matching with word boundaries
- Handle special cases like "go" programming language
- Add synonym normalization (js→javascript, py→python)
- Use intersection-only matching (no union)
- Add model fallback: gemini-pro → gemini-1.5-flash → gemini-2.0-flash-exp
```

### Similarity Scoring Formula
```
Implement weighted similarity scoring:
- Semantic similarity: 60% weight
- Skills overlap: 40% weight
- Penalties:
  - Missing required skills: -0.05 per skill
  - Off-topic skills: -0.02 per skill
- Final score clipped to [0, 1]
- Shortlist threshold: 80%
```

### NumPy Removal
```
Remove NumPy dependency from agent1_service.py:
- Replace np.exp with math.exp
- Use Python built-in functions for calculations
- Maintain same functionality without external dependencies
```

---

## Agent 2: Interview Scheduling Prompts

### Database Schema Design
```
Create PostgreSQL database schema:
- Panel table: id, name, expertise, busy_until
- Candidate table: id, name, email, status, created_at
- Interview table: id, candidate_id, panel_id, scheduled_at, status
- Relationships: Interview → Candidate, Interview → Panel
```

### Panel Assignment Logic
```
Implement deterministic panel assignment:
1. Priority 1: Panels with NULL busy_until (never scheduled)
2. Priority 2: Panels that are currently free
3. Priority 3: Panel with earliest busy_until time
4. Update panel's busy_until after assignment
5. Update candidate status to "scheduled"
```

### API Endpoints
```
Create scheduling endpoints:
- POST /api/agent2/schedule: Schedule interview for shortlisted candidate
- Input: candidate_id, interview_datetime
- Output: interview_id, panel_name, panel_expertise, scheduled_at
```

---

## Frontend Development Prompts

### Agent 1 UI
```
Build React component for Agent 1:
- File upload for JD and Resume (PDF/TXT)
- Display similarity results with match percentage
- Show extracted skills comparison
- Display candidate info (ID, name, status)
- Add localStorage persistence for results
```

### Agent 2 UI
```
Build React component for Agent 2:
- Input field for candidate ID (auto-filled from Agent 1)
- DateTime picker for interview scheduling
- Display scheduled interview details
- Show panel information
- Add localStorage persistence for scheduled interviews
```

### Navigation
```
Create tab-based navigation:
- Switch between Agent 1 and Agent 2
- Maintain state across navigation
- Highlight active tab
```

---

## Integration Prompts

### Candidate Creation in Agent 1
```
Integrate Agent 1 with database:
- Extract candidate name and email from resume using regex
- Create/update candidate record in database
- Return candidate_id in API response
- Display candidate info in frontend results
```

### Auto-fill Candidate ID in Agent 2
```
Connect Agent 1 and Agent 2:
- Store Agent 1 results in localStorage
- Auto-load candidate_id in Agent 2 from localStorage
- Pre-fill candidate ID input field
- Clear localStorage on reset
```

### Data Persistence
```
Add localStorage persistence:
- Agent 1: Save evaluation results on successful upload
- Agent 2: Save scheduled interview details
- Load data on component mount
- Persist across page refreshes and navigation
```

---

## Configuration Prompts

### Environment Setup
```
Configure backend environment:
- PostgreSQL connection: DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/interview_assistant
- Gemini API key: GEMINI_API_KEY=your_key_here
- Backend port: 8001 (not 8000)
```

### Database Initialization
```
Create database initialization script:
- Create all tables using SQLAlchemy models
- Seed 5 initial panels with different expertise
- Run: python backend/init_db.py
```

### Dependencies
```
Install required packages:
- Backend: fastapi, uvicorn, sqlalchemy, psycopg2-binary, google-generativeai, PyPDF2
- Frontend: react, axios, react-router-dom
- Upgrade SQLAlchemy to 2.0.48 for Python 3.13 compatibility
```

---

## Styling Prompts

### CSS Design
```
Create comprehensive styling:
- Navigation tabs with hover effects
- File upload area with drag-and-drop styling
- Results cards with grid layout
- Skills comparison with color-coded badges
- Candidate info section with status badges
- Scheduling form with modern input fields
- Responsive design for all screen sizes
```

---

## Testing Prompts

### End-to-End Flow
```
Test complete workflow:
1. Upload JD and Resume in Agent 1
2. Verify similarity calculation and skills extraction
3. Check candidate creation in database
4. Navigate to Agent 2
5. Verify candidate ID auto-fill
6. Schedule interview
7. Verify panel assignment and database updates
8. Test data persistence across page refreshes
```

---

## Optimization Prompts

### Performance
```
Optimize application performance:
- Remove FAISS dependency (Python 3.13 compatibility)
- Use simple cosine similarity instead
- Implement proper session scoping in vector_repo
- Add model fallback for skills extraction
- Minimize API calls with caching
```

### Error Handling
```
Add robust error handling:
- File parsing errors (PDF/TXT)
- Database connection errors
- Gemini API failures with fallback models
- Invalid candidate ID in scheduling
- Panel availability conflicts
```
