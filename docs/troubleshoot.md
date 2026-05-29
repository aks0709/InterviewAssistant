# Interview Assistant - Troubleshooting Guide

## Issues Faced and Solutions

---

## 1. FAISS Dependency Compatibility Issue

### Problem
- FAISS library not compatible with Python 3.13
- Installation failed with compilation errors
- Blocked vector similarity implementation

### Why It Occurred
- FAISS requires specific C++ compiler versions
- Python 3.13 is too new for current FAISS builds
- No pre-built wheels available for Python 3.13 on Windows

### Solution
- Removed FAISS dependency completely
- Implemented simple cosine similarity using Python built-ins
- Created custom vector_repo.py with manual similarity calculation
- Formula: `cosine_similarity = dot_product / (norm_a * norm_b)`

### Code Changes
```python
# backend/app/repository/vector_repo.py
def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0
```

---

## 2. NumPy Dependency in Agent1 Service

### Problem
- agent1_service.py used `np.exp()` for exponential calculations
- Added unnecessary NumPy dependency
- Increased package size and installation complexity

### Why It Occurred
- Initial implementation copied from examples using NumPy
- Didn't consider Python's built-in math module

### Solution
- Replaced `np.exp()` with `math.exp()`
- Used Python built-in functions for all calculations
- Removed NumPy import completely

### Code Changes
```python
# Before
import numpy as np
semantic_sim = np.exp(raw_sim) / (1 + np.exp(raw_sim))

# After
import math
semantic_sim = math.exp(raw_sim) / (1 + math.exp(raw_sim))
```

---

## 3. Gemini Embedding Model Name Error

### Problem
- Used incorrect model name: "gemini-pro" for embeddings
- API returned error: "Model not found"
- Embeddings generation failed

### Why It Occurred
- Confusion between text generation models and embedding models
- Gemini has separate models for different tasks

### Solution
- Changed to correct embedding model: "models/gemini-embedding-001"
- Updated all embedding calls in agent1_service.py

### Code Changes
```python
# Correct embedding model
embedding = genai.embed_content(
    model="models/gemini-embedding-001",
    content=text,
    task_type="retrieval_document"
)
```

---

## 4. Skills Extraction Inaccuracy

### Problem
- Skills extraction using simple string matching was inaccurate
- Partial matches caused false positives (e.g., "go" matching "golang")
- Skills like "react" matched "reactive programming"

### Why It Occurred
- Used substring matching without word boundaries
- No context awareness in matching logic

### Solution
- Implemented LLM-based skills extraction using Gemini
- Added atomic skill matching with word boundaries using regex
- Special handling for "go" programming language
- Synonym normalization (js→javascript, py→python)
- Model fallback strategy for reliability

### Code Changes
```python
# backend/app/services/skills_extractor.py
def extract_skills_with_llm(text: str) -> List[str]:
    models = ["gemini-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"]
    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            # Parse and return skills
        except Exception:
            continue
```

---

## 5. Similarity Scoring Too Lenient

### Problem
- Initial scoring gave high matches even for poor resumes
- No penalties for missing required skills
- Off-topic skills inflated scores

### Why It Occurred
- Simple averaging of semantic and skills similarity
- No consideration of skill gaps or irrelevant skills

### Solution
- Implemented weighted scoring: 60% semantic + 40% skills
- Added penalties:
  - Missing required skills: -0.05 per skill
  - Off-topic skills: -0.02 per skill
- Clipped final score to [0, 1] range
- Set shortlist threshold at 80%

### Code Changes
```python
final_score = 0.60 * semantic_sim + 0.40 * skills_overlap
final_score -= (penalty_required + penalty_offtopic)
final_score = max(0.0, min(1.0, final_score))
```

---

## 6. SQLAlchemy Version Compatibility

### Problem
- SQLAlchemy 1.x not compatible with Python 3.13
- Import errors and deprecated API usage

### Why It Occurred
- Python 3.13 removed some deprecated features
- SQLAlchemy 1.x relied on those features

### Solution
- Upgraded to SQLAlchemy 2.0.48
- Updated psycopg2-binary to 2.9.11
- Modified database session management for SQLAlchemy 2.x

### Code Changes
```bash
pip install --upgrade sqlalchemy==2.0.48 psycopg2-binary==2.9.11
```

---

## 7. Vector Repository Session Contamination

### Problem
- Vector similarity results contaminated across different requests
- Session data persisted between API calls

### Why It Occurred
- Improper session scoping in vector_repo.py
- Shared state between requests

### Solution
- Implemented proper session isolation
- Each similarity calculation uses fresh data
- No shared state between requests

### Code Changes
```python
def compute_similarity(self, vec_a, vec_b):
    # Use local variables only, no class state
    return self.cosine_similarity(vec_a, vec_b)
```

---

## 8. DOCX File Parsing Dependency Issue

### Problem
- python-docx library installation failed
- Blocked DOCX file support

### Why It Occurred
- python-docx has complex dependencies
- Compatibility issues with Python 3.13

### Solution
- Removed DOCX support from file_parser.py
- Focused on PDF and TXT only (most common formats)
- Documented limitation in README

### Code Changes
```python
# Removed DOCX parsing code
# Kept only PDF (PyPDF2) and TXT support
```

---

## 9. Backend Port Conflict

### Problem
- Backend configured for port 8000 but run.bat used 8001
- Frontend API calls failed with connection errors

### Why It Occurred
- Mismatch between documentation and actual configuration
- Port 8000 might be in use by other services

### Solution
- Standardized on port 8001 across all configurations
- Updated frontend API base URL to http://localhost:8001
- Updated all documentation

### Code Changes
```javascript
// frontend/src/components/Agent1Similarity.jsx
const response = await axios.post('http://localhost:8001/api/agent1/evaluate', formData);
```

---

## 10. Candidate Name/Email Extraction

### Problem
- No automatic extraction of candidate information from resume
- Manual entry required in database

### Why It Occurred
- Initial implementation focused only on similarity scoring
- Didn't consider candidate management workflow

### Solution
- Added regex-based extraction for name and email
- Name: First line or "Name:" field in resume
- Email: Standard email regex pattern
- Fallback to "Unknown" if not found

### Code Changes
```python
# backend/app/routes/agent1.py
name_match = re.search(r'(?:Name|name):\s*([^\n]+)', resume_text)
email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume_text)
```

---

## 11. Frontend State Persistence

### Problem
- Data lost on page refresh or navigation between agents
- Poor user experience with repeated data entry

### Why It Occurred
- React state is ephemeral and doesn't persist
- No storage mechanism implemented

### Solution
- Implemented localStorage for data persistence
- Agent 1: Save evaluation results
- Agent 2: Save scheduled interviews
- Load data on component mount
- Clear on reset/logout

### Code Changes
```javascript
// Save to localStorage
localStorage.setItem('agent1Results', JSON.stringify(results));

// Load from localStorage
const [results, setResults] = useState(() => {
    const saved = localStorage.getItem('agent1Results');
    return saved ? JSON.parse(saved) : null;
});
```

---

## 12. Panel Assignment Logic Ambiguity

### Problem
- Multiple panels available, unclear which to assign
- Non-deterministic assignment caused testing issues

### Why It Occurred
- No clear priority rules for panel selection
- Random selection not suitable for production

### Solution
- Implemented deterministic 3-tier priority system:
  1. Panels with NULL busy_until (never scheduled)
  2. Panels currently free (busy_until < now)
  3. Panel with earliest busy_until time
- Consistent and predictable assignments

### Code Changes
```python
# backend/app/services/agent2_service.py
def assign_panel(self, interview_datetime):
    # Priority 1: NULL busy_until
    # Priority 2: Free panels
    # Priority 3: Earliest busy_until
```

---

## 13. Skills Matching Union vs Intersection

### Problem
- Using union for skills matching inflated scores
- Resumes with many irrelevant skills got high scores

### Why It Occurred
- Initial implementation used (matched / (jd_skills ∪ resume_skills))
- Union includes all skills from both documents

### Solution
- Changed to intersection-only matching
- Formula: matched_skills / jd_required_skills
- Only JD skills matter for scoring
- Resume-only skills don't inflate score

### Code Changes
```python
# Use intersection only
skills_overlap = len(matched_skills) / len(jd_skills) if jd_skills else 0.0
```

---

## 14. Database Connection String Format

### Problem
- PostgreSQL connection failed with authentication errors
- Incorrect connection string format

### Why It Occurred
- Missing password in DATABASE_URL
- Incorrect syntax for PostgreSQL URL

### Solution
- Corrected format: `postgresql://user:password@host:port/database`
- Added password to .env file
- Verified connection with psql client

### Code Changes
```bash
# backend/.env
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/interview_assistant
```

---

## 15. React Component Re-rendering Issues

### Problem
- Components re-rendering unnecessarily
- Performance degradation with large result sets

### Why It Occurred
- Missing dependency arrays in useEffect
- State updates triggering cascading re-renders

### Solution
- Added proper dependency arrays to useEffect hooks
- Memoized expensive calculations
- Used functional state updates

### Code Changes
```javascript
useEffect(() => {
    // Load from localStorage only on mount
}, []); // Empty dependency array
```

---

## Common Debugging Commands

### Backend
```bash
# Check if backend is running
curl http://localhost:8001/

# Test Agent 1 endpoint
curl -X POST http://localhost:8001/api/agent1/evaluate -F "jd=@jd.pdf" -F "resume=@resume.pdf"

# Check database connection
python -c "from backend.app.models.database import engine; print(engine.connect())"
```

### Frontend
```bash
# Check if frontend is running
curl http://localhost:5173/

# Clear localStorage
# Open browser console: localStorage.clear()
```

### Database
```bash
# Connect to PostgreSQL
psql -U postgres -d interview_assistant

# Check tables
\dt

# View candidates
SELECT * FROM candidates;

# View panels
SELECT * FROM panels;
```

---

## Prevention Tips

1. **Always check Python version compatibility** before installing packages
2. **Use virtual environments** to isolate dependencies
3. **Test API endpoints** with curl before frontend integration
4. **Validate database connections** before running migrations
5. **Use proper error handling** with try-catch blocks
6. **Implement logging** for debugging production issues
7. **Document all configuration** in .env.example files
8. **Test edge cases** (empty files, missing fields, etc.)
9. **Use TypeScript** for better type safety in frontend
10. **Implement health check endpoints** for monitoring

---

## Future Improvements

1. Add comprehensive error messages to frontend
2. Implement retry logic for API calls
3. Add loading states for better UX
4. Implement proper authentication and authorization
5. Add unit tests for all services
6. Implement CI/CD pipeline
7. Add monitoring and alerting
8. Optimize database queries with indexes
9. Implement caching for embeddings
10. Add support for more file formats (DOCX, DOC)
