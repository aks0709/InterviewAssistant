# Interview Assistant - High-Level Design (HLD)

## 1. System Overview

Interview Assistant is a RAG-based backend system that evaluates candidates through three specialized agents:
- **Agent 1:** JD-Resume Similarity Matching
- **Agent 2:** Interview Scheduling (Planned)
- **Agent 3:** Interview Question Generation (Planned)

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 3000)                   │
│                    (Not implemented yet)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8001)                     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    CORS Middleware                        │   │
│  │              (Allow localhost:3000)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Agent 1     │  │  Agent 2     │  │  Agent 3     │           │
│  │  Similarity  │  │  Scheduling  │  │  Questions   │           │
│  │  /evaluate   │  │  /schedule   │  │  /questions  │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                    │
│         ▼                 ▼                 ▼                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Service Layer                               │   │
│  │  ┌─────────────────────────────────────────────────────┐ │   │
│  │  │ Agent1Service  │ Agent2Service  │ Agent3Service     │ │   │
│  │  └─────────────────────────────────────────────────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Repository Layer                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │ VectorRepo   │  │ DatabaseRepo │  │ HistoryRepo  │   │   │
│  │  │ (FAISS)      │  │ (PostgreSQL) │  │ (JSON Files) │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Utility Layer                               │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │ Chunking     │  │ Embeddings   │  │ Config       │   │   │
│  │  │ (Text Split) │  │ (Gemini API) │  │ (.env)       │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │   Gemini    │    │   FAISS     │    │ PostgreSQL  │
   │   API       │    │   Vector DB │    │ Database    │
   │ (Embeddings)│    │ (Local)     │    │ (Optional)  │
   └─────────────┘    └─────────────┘    └─────────────┘
```

---

## 3. Technology Stack

### Backend Framework
- **FastAPI 0.109.0** - Modern async web framework
- **Uvicorn 0.27.0** - ASGI server
- **Python 3.11+** - Programming language

### AI/ML Stack
- **LangChain 1.2.10** - LLM orchestration framework
- **Google Generative AI 0.4.1** - Gemini API SDK
- **LangChain-Google-GenAI 4.2.1** - LangChain integration

### Vector Database
- **FAISS 1.9.0.post1** - Facebook AI Similarity Search
  - Local in-memory vector store
  - L2 distance metric for similarity
  - Persists to disk after each evaluation

### Data & Configuration
- **Pydantic 2.12.5** - Data validation
- **Pydantic-Settings 2.13.1** - Environment configuration
- **python-dotenv 1.0.0** - .env file loading

### Database (Optional for Agent 2)
- **SQLAlchemy 2.0.25** - ORM
- **psycopg2-binary 2.9.11** - PostgreSQL driver

### Document Processing
- **PyPDF2 3.0.1** - PDF parsing
- **python-docx 1.1.0** - DOCX parsing

### Utilities
- **NumPy 2.4.3** - Numerical operations
- **scikit-learn 1.8.0** - ML utilities

---

## 4. Models & APIs Used

### Gemini Models

#### 1. Embedding Model: `models/embedding-001`
- **Purpose:** Convert text to 768-dimensional vectors
- **Use Case:** Similarity search between JD and Resume
- **Dimension:** 768
- **Task Type:** `retrieval_document`
- **Why:** 
  - Free tier available
  - High-quality embeddings
  - Optimized for semantic search
  - Supports batch processing

#### 2. LLM Model: `gemini-2.5-flash` (Planned for Agent 3)
- **Purpose:** Generate interview questions
- **Why:**
  - Fast inference
  - Cost-effective
  - Good for text generation
  - Supports context windows

---

## 5. Agent Communication & Synchronization

### Agent 1: JD-Resume Similarity (IMPLEMENTED)

**Flow:**
```
Request → Chunking → Embeddings → FAISS Search → Scoring → Response
```

**Input:**
```json
{
  "jd_text": "string",
  "resume_text": "string"
}
```

**Output:**
```json
{
  "similarity_score": 0.85,
  "matched_topics": [...],
  "decision": "shortlisted",
  "threshold": 0.80
}
```

**Synchronization:** Stateless - each request is independent

---

### Agent 2: Interview Scheduling (PLANNED)

**Flow:**
```
Request → Validate → Check Availability → Store in DB → Response
```

**Synchronization:** 
- Reads from PostgreSQL
- Writes scheduling records
- Coordinates with Agent 1 results

---

### Agent 3: Interview Questions (PLANNED)

**Flow:**
```
Request → Load Context → Generate with LLM → Store History → Response
```

**Synchronization:**
- Receives Agent 1 similarity score
- Uses Agent 2 scheduling info
- Generates contextual questions

---

## 6. Data Flow

### Agent 1 Detailed Flow

```
1. INPUT VALIDATION
   ├─ Check jd_text not empty
   └─ Check resume_text not empty

2. TEXT CHUNKING
   ├─ Split JD into 500-char chunks (50-char overlap)
   ├─ Split Resume into 500-char chunks (50-char overlap)
   └─ Remove empty chunks

3. EMBEDDING GENERATION
   ├─ Call Gemini embedding-001 API
   ├─ Generate 768-dim vectors for each chunk
   └─ Batch process for efficiency

4. VECTOR STORAGE
   ├─ Create FAISS index (L2 distance)
   ├─ Add JD embeddings to index
   └─ Store metadata (text, type)

5. SIMILARITY SEARCH
   ├─ For each Resume chunk:
   │  ├─ Search top-3 similar JD chunks
   │  ├─ Calculate L2 distance
   │  └─ Convert to similarity score
   └─ Collect all scores

6. SCORING
   ├─ Calculate average similarity
   ├─ Extract high-confidence matches (>0.7)
   └─ Normalize to 0-1 range

7. DECISION
   ├─ If score >= 0.80 → "shortlisted"
   └─ Else → "rejected"

8. PERSISTENCE
   ├─ Save FAISS index to disk
   ├─ Save metadata pickle file
   └─ Optional: Save history JSON
```

---

## 7. Storage Architecture

### Vector Database (FAISS)

**Location:** `backend/data/faiss_index/`

**Files:**
- `index.faiss` - Binary FAISS index
- `metadata.pkl` - Python pickle with text chunks

**Characteristics:**
- In-memory during request
- Persisted to disk after evaluation
- Recreated for each new evaluation (stateless)
- No external service required

**Why FAISS:**
- Fast similarity search
- Minimal dependencies
- Local storage (no cloud costs)
- Suitable for small-medium datasets

### Conversation History (Optional)

**Location:** `backend/data/history/`

**Format:** JSON files with timestamp

**Structure:**
```json
{
  "timestamp": "2024-01-15T14:30:22",
  "jd_text": "...",
  "resume_text": "...",
  "similarity_score": 0.85,
  "matched_topics": [...],
  "decision": "shortlisted"
}
```

**Purpose:**
- Track evaluation history
- Analytics and reporting
- Candidate re-evaluation

---

## 8. Configuration Management

### Environment Variables (.env)

```env
# Gemini API Key (Required)
GOOGLE_API_KEY=your_actual_key

# Database (Optional for Agent 2)
DATABASE_URL=postgresql://user:password@localhost:5432/interview_assistant

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Why .env:**
- Never hardcode secrets
- Easy environment switching
- Secure credential management
- Follows 12-factor app principles

---

## 9. API Endpoints

### Agent 1: Similarity Evaluation

**Endpoint:** `POST /agent1/evaluate`

**Request:**
```json
{
  "jd_text": "Job description text",
  "resume_text": "Resume text"
}
```

**Response:**
```json
{
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

**Status Codes:**
- `200` - Success
- `400` - Invalid input
- `500` - Server error

---

### Agent 2: Scheduling (PLANNED)

**Endpoint:** `POST /agent2/schedule`

**Endpoint:** `GET /agent2/schedule/{interview_id}`

---

### Agent 3: Questions (PLANNED)

**Endpoint:** `POST /agent3/questions`

**Endpoint:** `POST /agent3/questions/followup`

---

## 10. Security Considerations

1. **API Key Management**
   - Stored in `.env` file
   - Never committed to git
   - Loaded via pydantic-settings

2. **CORS Configuration**
   - Restricted to `http://localhost:3000`
   - Configurable via environment

3. **Input Validation**
   - Pydantic schemas validate all inputs
   - Type checking enforced

4. **Error Handling**
   - Graceful error responses
   - No sensitive data in error messages

---

## 11. Performance Considerations

### Chunking Strategy
- **Size:** 500 characters
- **Overlap:** 50 characters
- **Reason:** Balance between granularity and efficiency

### Embedding Batch Processing
- Process multiple chunks in single API call
- Reduces API latency
- Efficient token usage

### FAISS Optimization
- L2 distance metric (fast)
- In-memory search (no I/O)
- Suitable for <1M vectors

### Caching (Future)
- Cache embeddings for repeated documents
- Redis integration ready
- Reduces API calls

---

## 12. Scalability Path

### Current (MVP)
- Single-threaded requests
- In-memory FAISS
- File-based history

### Phase 2
- Async request processing
- Redis caching
- PostgreSQL for history

### Phase 3
- Distributed FAISS indices
- Message queue (Celery)
- Microservices architecture

---

## 13. Dependencies Justification

| Package | Version | Purpose | Why |
|---------|---------|---------|-----|
| FastAPI | 0.109.0 | Web framework | Modern, async, auto-docs |
| Uvicorn | 0.27.0 | ASGI server | Production-ready |
| LangChain | 1.2.10 | LLM orchestration | Unified API for LLMs |
| google-generativeai | 0.4.1 | Gemini SDK | Official Google SDK |
| FAISS | 1.9.0.post1 | Vector search | Fast, local, no deps |
| Pydantic | 2.12.5 | Data validation | Type-safe, auto-docs |
| python-dotenv | 1.0.0 | Config management | Secure secrets |
| SQLAlchemy | 2.0.25 | ORM | For Agent 2 (DB) |
| PyPDF2 | 3.0.1 | PDF parsing | Document processing |

---

## 14. Monitoring & Logging (Future)

```python
# Planned logging structure
{
  "timestamp": "2024-01-15T14:30:22",
  "agent": "agent1",
  "endpoint": "/agent1/evaluate",
  "status": "success",
  "duration_ms": 1234,
  "similarity_score": 0.85,
  "decision": "shortlisted"
}
```

---

## 15. Testing Strategy

### Unit Tests
- Chunking logic
- Embedding generation
- Similarity calculation

### Integration Tests
- Full Agent 1 flow
- API endpoint testing
- FAISS operations

### Load Tests
- Concurrent requests
- Large document handling
- API rate limiting

---

## 16. Deployment Considerations

### Development
```bash
cd backend
run.bat  # Windows
# or
./run.sh  # Linux/Mac
```

### Production
- Use production ASGI server (Gunicorn)
- Enable HTTPS
- Set `ENVIRONMENT=production`
- Use managed PostgreSQL
- Implement monitoring

---

## 17. Future Enhancements

1. **Agent 2 Implementation**
   - PostgreSQL integration
   - Calendar API integration
   - Conflict resolution

2. **Agent 3 Implementation**
   - Context-aware question generation
   - Difficulty level adjustment
   - Follow-up question logic

3. **Advanced Features**
   - Multi-language support
   - Resume parsing (OCR)
   - Skill extraction
   - Candidate ranking

4. **Infrastructure**
   - Docker containerization
   - Kubernetes deployment
   - CI/CD pipeline
   - Monitoring & alerting

---

## 18. Conclusion

Interview Assistant is a modular, scalable RAG system built with modern Python technologies. Agent 1 demonstrates the core pattern: chunking → embedding → vector search → scoring. This architecture supports easy addition of Agent 2 and Agent 3 while maintaining clean separation of concerns.

**Key Strengths:**
- ✓ Modular design
- ✓ No external dependencies (FAISS local)
- ✓ Secure configuration
- ✓ Type-safe with Pydantic
- ✓ Production-ready FastAPI
- ✓ Extensible for future agents
