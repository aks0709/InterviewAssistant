# Agent 3: Interview Question Generator

## Overview
Agent 3 generates interview questions based on overlapping skills between Job Description and Resume (from Agent 1 evaluation). Uses Gemini Flash 2.5 LLM to create 15 questions across 3 difficulty levels.

---

## Architecture

### Components

1. **Service Layer** (`backend/app/services/agent3/agent3_service.py`)
   - `Agent3Service`: Core question generation logic
   - Uses Gemini Flash 2.5 (`gemini-2.0-flash-exp`)
   - Prompt engineering for structured output
   - JSON parsing and validation

2. **API Layer** (`backend/app/routes/agent3.py`)
   - Endpoint: `POST /agent3/questions`
   - Validates candidate exists and has been evaluated
   - Fetches overlapping skills from database
   - Returns generated questions

3. **Database Layer** (`backend/app/models/database.py`)
   - Added `overlapping_skills` TEXT field to Candidate model
   - Stores JSON array of matched skills from Agent 1

---

## Flow Diagram

```
User Request
    ↓
POST /agent3/questions
    ↓
Validate candidate_id
    ↓
Fetch candidate from DB
    ↓
Check if evaluated (Agent 1)
    ↓
Extract overlapping_skills (JSON)
    ↓
Agent3Service.generate_questions()
    ↓
Build prompt with skills + custom requirements
    ↓
Call Gemini Flash 2.5 LLM
    ↓
Parse JSON response
    ↓
Validate structure (easy/medium/hard)
    ↓
Return questions + metadata
```

---

## Prompt Template

The LLM prompt is structured as follows:

```
You are an expert technical interviewer. Generate interview questions based on the following skills that overlap between the job description and candidate's resume.

**Skills to focus on:** [comma-separated skills]

**Requirements:**
1. Generate exactly 5 EASY questions (basic concepts, definitions, simple scenarios)
2. Generate exactly 5 MEDIUM questions (practical application, problem-solving, moderate complexity)
3. Generate exactly 5 HARD questions (advanced concepts, system design, complex scenarios, edge cases)

4. Questions should be:
   - Relevant to the specific skills listed
   - Progressive in difficulty
   - Practical and realistic for actual interviews
   - Clear and unambiguous
   - Cover different aspects of each skill

[If custom_requirements provided:]
**Additional Requirements from Interviewer:**
[custom requirements text]

Please incorporate these specific requirements into the questions.

**Output Format (JSON):**
{
  "easy": ["Q1", "Q2", "Q3", "Q4", "Q5"],
  "medium": ["Q1", "Q2", "Q3", "Q4", "Q5"],
  "hard": ["Q1", "Q2", "Q3", "Q4", "Q5"]
}

Generate ONLY the JSON output, no additional text.
```

---

## API Specification

### Endpoint
```
POST /agent3/questions
```

### Request Body
```json
{
  "candidate_id": 123,
  "custom_requirements": "Focus on React hooks and state management" // Optional
}
```

### Response (Success)
```json
{
  "questions": {
    "easy": [
      "What is the difference between let and var in JavaScript?",
      "Explain what React components are.",
      "What is the purpose of useState hook?",
      "How do you create a basic REST API endpoint?",
      "What is SQL used for?"
    ],
    "medium": [
      "How would you optimize a React component that re-renders frequently?",
      "Explain the difference between useEffect and useLayoutEffect.",
      "Design a simple authentication system using JWT.",
      "How do you handle race conditions in async JavaScript?",
      "Write a SQL query to find duplicate records."
    ],
    "hard": [
      "Design a scalable real-time notification system using React and WebSockets.",
      "Explain how React's reconciliation algorithm works internally.",
      "How would you implement server-side rendering with React?",
      "Design a database schema for a multi-tenant SaaS application.",
      "Implement a custom React hook for debouncing API calls."
    ]
  },
  "skills": ["JavaScript", "React", "SQL", "REST API"],
  "custom_requirements": "Focus on React hooks and state management",
  "candidate_id": 123,
  "candidate_name": "John Doe",
  "candidate_email": "john@example.com"
}
```

### Error Responses

**404 - Candidate Not Found**
```json
{
  "detail": "Candidate with ID 123 not found"
}
```

**400 - Not Evaluated**
```json
{
  "detail": "Candidate has not been evaluated yet. Please run Agent 1 first."
}
```

**400 - No Skills**
```json
{
  "detail": "No overlapping skills found for this candidate. Cannot generate questions."
}
```

**500 - Generation Error**
```json
{
  "detail": "Error generating questions: [error message]"
}
```

---

## Configuration

### Environment Variables

Agent 3 loads configuration from `.env` file:

```bash
# backend/.env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/interview_assistant
```

**Key Loading:**
- `GEMINI_API_KEY` is loaded in `Agent3Service.__init__()` using `os.getenv()`
- Raises `ValueError` if key is not found
- Never hardcoded in source code

---

## Execution Steps

### 1. Database Migration (One-time)

Add `overlapping_skills` column to existing database:

```bash
cd c:\Users\akum1183\OneDrive - Capgemini\Desktop\InterviewAssistant
python backend/migrate_add_skills.py
```

Or recreate database:

```bash
python backend/init_db.py
```

### 2. Restart Backend

```bash
cd backend
run.bat
```

Backend will start on `http://localhost:8001`

### 3. Test Agent 3

**Step 1: Evaluate a candidate (Agent 1)**
```bash
curl -X POST http://localhost:8001/agent1/evaluate \
  -F "jd_file=@path/to/jd.pdf" \
  -F "resume_file=@path/to/resume.pdf"
```

Response will include `candidate_id`.

**Step 2: Generate questions (Agent 3)**
```bash
curl -X POST http://localhost:8001/agent3/questions \
  -H "Content-Type: application/json" \
  -d "{\"candidate_id\": 1}"
```

**Step 3: Generate with custom requirements**
```bash
curl -X POST http://localhost:8001/agent3/questions \
  -H "Content-Type: application/json" \
  -d "{\"candidate_id\": 1, \"custom_requirements\": \"Focus on system design and scalability\"}"
```

---

## Modular Architecture

### Separation of Concerns

1. **Service Layer** (`agent3_service.py`)
   - Pure business logic
   - No HTTP/database dependencies
   - Testable in isolation
   - Reusable across different interfaces

2. **API Layer** (`agent3.py`)
   - HTTP request/response handling
   - Input validation
   - Database queries
   - Error handling

3. **Data Layer** (`database.py`)
   - Database models
   - Schema definitions
   - No business logic

### Benefits

- **Testability**: Each layer can be tested independently
- **Maintainability**: Changes in one layer don't affect others
- **Reusability**: Service can be used by CLI, API, or other interfaces
- **Security**: API keys loaded from environment, never hardcoded

---

## Custom Requirements Feature

Users can specify custom requirements to tailor questions:

### Examples

**Focus on specific topics:**
```json
{
  "candidate_id": 1,
  "custom_requirements": "Focus on React hooks, especially useEffect and custom hooks"
}
```

**Scenario-based questions:**
```json
{
  "candidate_id": 1,
  "custom_requirements": "Include real-world scenarios from e-commerce applications"
}
```

**Specific difficulty adjustments:**
```json
{
  "candidate_id": 1,
  "custom_requirements": "Make hard questions focus on system design and architecture"
}
```

**Domain-specific:**
```json
{
  "candidate_id": 1,
  "custom_requirements": "Questions should be relevant to fintech and payment processing"
}
```

---

## Error Handling

### LLM Failures

If Gemini API fails, the service:
1. Logs the error
2. Returns fallback error messages
3. Raises exception to API layer

### JSON Parsing Failures

If LLM returns invalid JSON:
1. Attempts to clean markdown code blocks
2. Validates required keys (easy/medium/hard)
3. Returns error messages if parsing fails

### Database Failures

If candidate not found or skills missing:
1. Returns appropriate HTTP error codes
2. Provides clear error messages
3. Logs for debugging

---

## Testing

### Manual Testing

```bash
# Test with valid candidate
curl -X POST http://localhost:8001/agent3/questions \
  -H "Content-Type: application/json" \
  -d "{\"candidate_id\": 1}"

# Test with invalid candidate
curl -X POST http://localhost:8001/agent3/questions \
  -H "Content-Type: application/json" \
  -d "{\"candidate_id\": 999}"

# Test with custom requirements
curl -X POST http://localhost:8001/agent3/questions \
  -H "Content-Type: application/json" \
  -d "{\"candidate_id\": 1, \"custom_requirements\": \"Focus on algorithms\"}"
```

### Expected Behavior

1. **Valid Request**: Returns 15 questions (5 easy, 5 medium, 5 hard)
2. **Invalid Candidate**: Returns 404 error
3. **Not Evaluated**: Returns 400 error
4. **No Skills**: Returns 400 error
5. **Custom Requirements**: Questions reflect the custom instructions

---

## Integration with Other Agents

### Agent 1 → Agent 3
- Agent 1 evaluates JD-Resume similarity
- Stores `overlapping_skills` in candidate record
- Agent 3 reads these skills to generate questions

### Agent 2 → Agent 3
- Agent 2 schedules interview
- Agent 3 generates questions for the interview
- Questions can be sent to panel before interview

### Complete Flow
```
Upload JD + Resume (Agent 1)
    ↓
Evaluate & Store Skills
    ↓
Generate Questions (Agent 3)
    ↓
Schedule Interview (Agent 2)
    ↓
Send Questions to Panel
```

---

## Future Enhancements

1. **Question Storage**: Save generated questions to database
2. **Question History**: Track which questions were used
3. **Answer Evaluation**: Agent 4 to evaluate candidate answers
4. **Question Bank**: Build reusable question library
5. **Difficulty Calibration**: Adjust based on candidate level
6. **Multi-language Support**: Generate questions in different languages
7. **Question Templates**: Pre-defined templates for common roles

---

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution**: Add key to `backend/.env` file

### Issue: "Candidate has not been evaluated"
**Solution**: Run Agent 1 first to evaluate the candidate

### Issue: "No overlapping skills found"
**Solution**: Check if Agent 1 stored skills correctly, or re-evaluate

### Issue: "Error generating questions"
**Solution**: Check Gemini API quota, network connection, and logs

### Issue: Column 'overlapping_skills' does not exist
**Solution**: Run migration script: `python backend/migrate_add_skills.py`

---

## Summary

Agent 3 is a modular, secure, and flexible question generation system that:
- ✓ Uses Gemini Flash 2.5 LLM
- ✓ Generates 15 questions (5 easy, 5 medium, 5 hard)
- ✓ Supports custom requirements
- ✓ Loads API keys from environment
- ✓ Clean separation of concerns
- ✓ Comprehensive error handling
- ✓ Integrates seamlessly with Agent 1 and Agent 2
