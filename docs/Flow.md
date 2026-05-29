# Interview Assistant - Agent Communication & Flow

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                          │
│                      http://localhost:3000                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    HTTP/REST (CORS Enabled)
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Port 8001)                   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Agent Orchestration Layer                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │   Agent 1    │  │   Agent 2    │  │   Agent 3    │  │    │
│  │  │ Similarity   │  │ Scheduling   │  │ Questions    │  │    │
│  │  │ (ACTIVE)     │  │ (PLANNED)    │  │ (PLANNED)    │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Shared Services Layer                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │ Embeddings   │  │ LLM Service  │  │ Config       │  │    │
│  │  │ (Gemini)     │  │ (Gemini)     │  │ (.env)       │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Data Persistence Layer                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │    │
│  │  │ FAISS Index  │  │ PostgreSQL   │  │ History JSON │  │    │
│  │  │ (Vector DB)  │  │ (Agent 2)    │  │ (Optional)   │  │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Agent 1: JD-Resume Similarity (IMPLEMENTED)

### 2.1 Endpoint
```
POST /agent1/evaluate
```

### 2.2 Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. FRONTEND REQUEST                                         │
│    {                                                        │
│      "jd_text": "Job description...",                       │
│      "resume_text": "Resume content..."                     │
│    }                                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. FASTAPI ROUTE (app/routes/agent1.py)                    │
│    - Validate request with Pydantic schema                 │
│    - Call Agent1Service.evaluate_similarity()              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. AGENT1SERVICE (app/services/agent1/agent1_service.py)   │
│    - Clear previous FAISS index                            │
│    - Call chunk_text() for JD                              │
│    - Call chunk_text() for Resume                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. TEXT CHUNKING (app/utils/chunks.py)                     │
│    JD Chunks:                                              │
│    ├─ Chunk 1: "We are looking for a Python developer..." │
│    ├─ Chunk 2: "with 3+ years of experience in..."        │
│    └─ Chunk 3: "FastAPI and machine learning"             │
│                                                            │
│    Resume Chunks:                                          │
│    ├─ Chunk 1: "Software Engineer with 5 years..."        │
│    ├─ Chunk 2: "Python experience. Built FastAPI..."      │
│    └─ Chunk 3: "ML models using scikit-learn"             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. EMBEDDING GENERATION (app/services/agent1/embeddings_service.py) │
│    Call: genai.embed_content(model="models/embedding-001") │
│                                                            │
│    JD Embeddings:                                          │
│    ├─ Emb 1: [0.12, 0.45, ..., 0.78] (768-dim)           │
│    ├─ Emb 2: [0.23, 0.56, ..., 0.89] (768-dim)           │
│    └─ Emb 3: [0.34, 0.67, ..., 0.90] (768-dim)           │
│                                                            │
│    Resume Embeddings:                                      │
│    ├─ Emb 1: [0.11, 0.44, ..., 0.77] (768-dim)           │
│    ├─ Emb 2: [0.22, 0.55, ..., 0.88] (768-dim)           │
│    └─ Emb 3: [0.33, 0.66, ..., 0.89] (768-dim)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. VECTOR STORAGE (app/repository/vector_repo.py)          │
│    - Create FAISS index (L2 distance metric)               │
│    - Add JD embeddings to index                            │
│    - Store metadata (text, type="jd")                      │
│                                                            │
│    FAISS Index State:                                      │
│    ├─ Dimension: 768                                       │
│    ├─ Vectors: 3 (JD chunks)                              │
│    └─ Metric: L2 (Euclidean distance)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. SIMILARITY SEARCH                                        │
│    For each Resume embedding:                              │
│    ├─ Search top-3 similar JD embeddings                   │
│    ├─ Calculate L2 distance                                │
│    └─ Convert to similarity score                          │
│                                                            │
│    Example:                                                │
│    Resume Chunk 1 vs JD:                                   │
│    ├─ Distance to JD Chunk 1: 0.15 → Similarity: 0.86    │
│    ├─ Distance to JD Chunk 2: 0.45 → Similarity: 0.64    │
│    └─ Distance to JD Chunk 3: 0.78 → Similarity: 0.46    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. SCORING & DECISION                                       │
│    - Calculate average similarity: 0.8523                  │
│    - Extract high-confidence matches (>0.7)               │
│    - Compare with threshold (0.80)                         │
│    - Decision: 0.8523 >= 0.80 → "shortlisted"            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. PERSISTENCE                                              │
│    - Save FAISS index to: backend/data/faiss_index/        │
│    - Save metadata pickle                                  │
│    - Optional: Save history JSON                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. RESPONSE                                                │
│     {                                                       │
│       "similarity_score": 0.8523,                           │
│       "matched_topics": [                                  │
│         {                                                  │
│           "resume_snippet": "Software Engineer...",        │
│           "jd_match": "We are looking for...",             │
│           "score": 0.89                                    │
│         }                                                  │
│       ],                                                   │
│       "decision": "shortlisted",                           │
│       "threshold": 0.80                                    │
│     }                                                       │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Data Structures

**Request:**
```python
class EvaluateRequest(BaseModel):
    jd_text: str
    resume_text: str
```

**Response:**
```python
class EvaluateResponse(BaseModel):
    similarity_score: float
    matched_topics: List[Dict]
    decision: str
    threshold: float
```

**Matched Topic:**
```python
{
    "resume_snippet": str,      # First 100 chars of resume chunk
    "jd_match": str,            # First 100 chars of JD chunk
    "score": float              # Similarity score (0-1)
}
```

---

## 3. Agent 2: Interview Scheduling (PLANNED)

### 3.1 Endpoint
```
POST /agent2/schedule
GET /agent2/schedule/{interview_id}
```

### 3.2 Planned Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. FRONTEND REQUEST                                         │
│    {                                                        │
│      "candidate_id": "123",                                 │
│      "preferred_dates": ["2024-01-20", "2024-01-21"],      │
│      "duration_minutes": 60                                 │
│    }                                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. AGENT2SERVICE                                            │
│    - Validate candidate exists (from Agent 1 result)       │
│    - Check interviewer availability                        │
│    - Find common time slots                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. DATABASE OPERATIONS (PostgreSQL)                         │
│    - Query: SELECT * FROM interviewers WHERE available     │
│    - Query: SELECT * FROM schedules WHERE date IN (...)    │
│    - Insert: INSERT INTO interviews (...)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. RESPONSE                                                 │
│    {                                                        │
│      "interview_id": "INT-001",                             │
│      "scheduled_date": "2024-01-20",                        │
│      "scheduled_time": "14:00",                             │
│      "interviewer": "John Doe",                             │
│      "duration_minutes": 60                                 │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Synchronization with Agent 1

```
Agent 1 Output → Agent 2 Input
├─ similarity_score → Used for priority ranking
├─ decision → Only "shortlisted" candidates scheduled
└─ matched_topics → Context for interviewer preparation
```

---

## 4. Agent 3: Interview Questions (PLANNED)

### 4.1 Endpoint
```
POST /agent3/questions
POST /agent3/questions/followup
```

### 4.2 Planned Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. FRONTEND REQUEST                                         │
│    {                                                        │
│      "interview_id": "INT-001",                             │
│      "difficulty_level": "medium",                          │
│      "num_questions": 5                                     │
│    }                                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. AGENT3SERVICE                                            │
│    - Load Agent 1 result (similarity, matched_topics)      │
│    - Load Agent 2 result (interview context)               │
│    - Build prompt with context                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. LLM CALL (Gemini 2.5 Flash)                              │
│    Prompt:                                                  │
│    "Generate 5 medium-difficulty interview questions       │
│     for a Python developer with FastAPI experience.        │
│     Focus on: [matched_topics from Agent 1]"               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. RESPONSE                                                 │
│    {                                                        │
│      "questions": [                                         │
│        {                                                    │
│          "id": 1,                                           │
│          "question": "Explain FastAPI middleware...",       │
│          "difficulty": "medium",                            │
│          "category": "FastAPI"                              │
│        },                                                   │
│        ...                                                  │
│      ]                                                      │
│    }                                                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Synchronization with Agent 1 & 2

```
Agent 1 Output → Agent 3 Input
├─ matched_topics → Question focus areas
├─ similarity_score → Difficulty adjustment
└─ decision → Only generate for "shortlisted"

Agent 2 Output → Agent 3 Input
├─ interview_id → Context linking
├─ interviewer → Interviewer preferences
└─ scheduled_date → Time-based context
```

---

## 5. Inter-Agent Communication Pattern

### 5.1 Data Flow Between Agents

```
┌──────────────┐
│   Agent 1    │
│ Similarity   │
└──────┬───────┘
       │
       │ Output:
       │ - similarity_score
       │ - matched_topics
       │ - decision
       │
       ▼
┌──────────────────────────────────────┐
│  Shared Context Store (Optional)     │
│  - Candidate Profile                 │
│  - Evaluation Results                │
│  - Interview Context                 │
└──────────────────────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Agent 2    │  │   Agent 3    │  │  Analytics   │
│ Scheduling   │  │  Questions   │  │  Dashboard   │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 5.2 Synchronization Mechanism

**Current (Agent 1 Only):**
- Stateless: Each request independent
- No inter-agent dependencies

**Future (All Agents):**
- Shared database for context
- Event-driven updates
- Message queue for async processing

---

## 6. Technology Choices & Justification

### 6.1 Embedding Model: `models/embedding-001`

**Why Gemini Embeddings:**
```
✓ Free tier available
✓ 768-dimensional vectors (good balance)
✓ Optimized for semantic search
✓ Supports batch processing
✓ No additional dependencies
✓ Integrated with Gemini ecosystem
```

**Alternative Considered:**
- HuggingFace (rejected: requires local model, larger dependencies)
- OpenAI (rejected: cost, external dependency)
- Cohere (rejected: less integrated)

### 6.2 Vector Database: FAISS

**Why FAISS:**
```
✓ Local in-memory storage (no external service)
✓ Fast similarity search (L2 distance)
✓ Minimal dependencies
✓ Suitable for MVP (< 1M vectors)
✓ Easy to persist to disk
✓ No cloud costs
```

**Alternative Considered:**
- Pinecone (rejected: cloud dependency, cost)
- Weaviate (rejected: complex setup)
- Milvus (rejected: requires Docker)
- Chroma (rejected: overkill for MVP)

### 6.3 LLM: Gemini 2.5 Flash

**Why Gemini 2.5 Flash:**
```
✓ Fast inference (suitable for real-time)
✓ Cost-effective
✓ Good for text generation
✓ Integrated with embedding model
✓ Supports context windows
✓ Reliable API
```

**Alternative Considered:**
- GPT-4 (rejected: cost, latency)
- Claude (rejected: cost)
- Llama (rejected: requires local setup)

### 6.4 Framework: FastAPI

**Why FastAPI:**
```
✓ Modern async framework
✓ Automatic API documentation (Swagger)
✓ Type safety with Pydantic
✓ High performance
✓ Easy to test
✓ Production-ready
```

**Alternative Considered:**
- Django (rejected: overkill, slower)
- Flask (rejected: no async, less type-safe)
- Starlette (rejected: lower-level)

### 6.5 SDK: google-generativeai

**Why Official Google SDK:**
```
✓ Official support
✓ Latest API features
✓ Reliable updates
✓ Good documentation
✓ Integrated with LangChain
```

---

## 7. Request/Response Flow Diagram

### 7.1 Complete Agent 1 Flow

```
Frontend                Backend                 External APIs
   │                       │                          │
   │ POST /agent1/evaluate │                          │
   ├──────────────────────>│                          │
   │                       │ Validate Request         │
   │                       │ (Pydantic)               │
   │                       │                          │
   │                       │ Chunk Text               │
   │                       │ (500 chars)              │
   │                       │                          │
   │                       │ Generate Embeddings      │
   │                       ├─────────────────────────>│
   │                       │ genai.embed_content()    │
   │                       │<─────────────────────────┤
   │                       │ [768-dim vectors]        │
   │                       │                          │
   │                       │ FAISS Search             │
   │                       │ (L2 distance)            │
   │                       │                          │
   │                       │ Calculate Similarity     │
   │                       │ (avg distance)           │
   │                       │                          │
   │                       │ Make Decision            │
   │                       │ (score >= 0.80?)         │
   │                       │                          │
   │                       │ Save FAISS Index         │
   │                       │ (to disk)                │
   │                       │                          │
   │ 200 OK                │                          │
   │ {response}            │                          │
   │<──────────────────────┤                          │
   │                       │                          │
```

---

## 8. Error Handling & Fallbacks

### 8.1 Agent 1 Error Scenarios

```
Error Case                  Handling
─────────────────────────────────────────────────────
Empty JD/Resume            → Return 400 Bad Request
API Key Invalid            → Return 500 Server Error
FAISS Index Corrupt        → Recreate index
Embedding API Timeout      → Retry with backoff
Invalid Similarity Score   → Default to 0.0
```

### 8.2 Agent 2 Error Scenarios (Planned)

```
Error Case                  Handling
─────────────────────────────────────────────────────
No Available Slots         → Return 404 Not Found
Database Connection Error  → Return 503 Service Unavailable
Conflict Resolution        → Suggest alternatives
```

### 8.3 Agent 3 Error Scenarios (Planned)

```
Error Case                  Handling
─────────────────────────────────────────────────────
LLM API Error              → Return 500 Server Error
Invalid Context            → Use default questions
Rate Limit Exceeded        → Queue request
```

---

## 9. Performance Metrics

### 9.1 Agent 1 Performance

```
Operation                   Time (Approx)
─────────────────────────────────────────
Text Chunking              ~10ms
Embedding Generation       ~500-1000ms (API call)
FAISS Search               ~50ms
Similarity Calculation     ~20ms
Total Request Time         ~600-1100ms
```

### 9.2 Optimization Opportunities

```
Current                     Optimization
─────────────────────────────────────────
Sequential API calls       → Batch embeddings
No caching                 → Redis cache
Single-threaded            → Async processing
```

---

## 10. Conversation History Structure

### 10.1 File-Based Storage

**Location:** `backend/data/history/`

**File Format:**
```
{timestamp}_{decision}.json
Example: 2024-01-15_143022_shortlisted.json
```

**Content:**
```json
{
  "timestamp": "2024-01-15T14:30:22",
  "jd_text": "Full JD text...",
  "resume_text": "Full resume text...",
  "similarity_score": 0.8523,
  "matched_topics": [
    {
      "resume_snippet": "...",
      "jd_match": "...",
      "score": 0.89
    }
  ],
  "decision": "shortlisted",
  "threshold": 0.80
}
```

### 10.2 Usage Scenarios

```
Scenario 1: Re-evaluation
├─ Load previous history file
├─ Compare with new evaluation
└─ Track changes over time

Scenario 2: Analytics
├─ Aggregate all history files
├─ Calculate acceptance rate
└─ Identify common patterns

Scenario 3: Audit Trail
├─ Track all evaluations
├─ Maintain compliance records
└─ Support appeals process
```

---

## 11. Future Enhancements

### 11.1 Agent Orchestration

```
Current: Independent agents
Future: Orchestrated workflow

Workflow:
1. Agent 1 evaluates similarity
2. If shortlisted → Agent 2 schedules
3. If scheduled → Agent 3 generates questions
4. All results → Analytics dashboard
```

### 11.2 Async Processing

```
Current: Synchronous requests
Future: Async with message queue

Flow:
1. Frontend submits request
2. Backend queues job
3. Worker processes asynchronously
4. WebSocket notifies frontend
```

### 11.3 Caching Strategy

```
Cache Layer:
├─ Embedding Cache (Redis)
│  └─ Key: hash(text) → Value: embedding
├─ FAISS Index Cache
│  └─ Persist frequently used indices
└─ LLM Response Cache
   └─ Cache common questions
```

---

## 12. Deployment Architecture

### 12.1 Development

```
Local Machine
├─ FastAPI (port 8001)
├─ FAISS (local disk)
├─ .env (local)
└─ Gemini API (cloud)
```

### 12.2 Production

```
Cloud Infrastructure
├─ Load Balancer
├─ FastAPI Instances (multiple)
├─ Redis Cache
├─ PostgreSQL Database
├─ FAISS Indices (distributed)
└─ Monitoring & Logging
```

---

## 13. Conclusion

Interview Assistant uses a modular, agent-based architecture where:

1. **Agent 1** (Implemented) - Evaluates JD-Resume similarity using Gemini embeddings and FAISS
2. **Agent 2** (Planned) - Schedules interviews using PostgreSQL
3. **Agent 3** (Planned) - Generates questions using Gemini LLM

Each agent is independent but can share context through a central data store. The system is designed for easy scaling and addition of new agents.

**Key Design Principles:**
- ✓ Modular: Each agent is independent
- ✓ Scalable: Easy to add new agents
- ✓ Secure: API keys in .env only
- ✓ Efficient: Async processing ready
- ✓ Maintainable: Clean separation of concerns
