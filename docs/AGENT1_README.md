# Agent 1: JD-Resume Similarity Evaluation

## Overview
Agent 1 evaluates similarity between Job Descriptions and Resumes using Gemini embeddings and FAISS vector search.

---

## 🔑 API Keys Configuration

### Location: `backend/.env`

```env
# Gemini API Key (for both embeddings and LLM)
GOOGLE_API_KEY=your_actual_gemini_api_key_here

# Database (for Agent 2)
DATABASE_URL=postgresql://user:password@localhost:5432/interview_assistant

# CORS
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**Get Gemini API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Create new API key
3. Copy and paste into `.env` file

---

## 📂 Vector DB Persistence

**Location:** `backend/data/faiss_index/`

Files:
- `index.faiss` - FAISS vector index
- `metadata.pkl` - Text chunks metadata

**Note:** Index is recreated for each evaluation (stateless per request)

---

## 🗂️ Conversation History Storage

**Structure:** File-based JSON storage

**Location:** `backend/data/history/` (optional - not implemented in minimal version)

**Format:**
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

**Note:** History storage is optional. Current implementation focuses on real-time evaluation.

---

## 🚀 Execution Steps

### 1. Setup Environment
```cmd
cd backend
start.bat
```

### 2. Configure API Key
Edit `backend/.env`:
```env
GOOGLE_API_KEY=your_actual_key
```

### 3. Start Server
Server runs at: `http://localhost:8001`

### 4. Test Agent 1

**Endpoint:** `POST /agent1/evaluate`

**Request:**
```json
{
  "jd_text": "We are looking for a Python developer with experience in FastAPI, machine learning, and cloud deployment. Must have 3+ years of experience.",
  "resume_text": "Software Engineer with 5 years of experience in Python, FastAPI, Django. Built ML models using scikit-learn and deployed on AWS."
}
```

**Response:**
```json
{
  "similarity_score": 0.8523,
  "matched_topics": [
    {
      "resume_snippet": "Software Engineer with 5 years of experience in Python, FastAPI, Django...",
      "jd_match": "We are looking for a Python developer with experience in FastAPI...",
      "score": 0.89
    }
  ],
  "decision": "shortlisted",
  "threshold": 0.80
}
```

### 5. API Documentation
Visit: `http://localhost:8001/docs`

---

## 📊 How It Works

1. **Chunking:** Documents split into 500-char chunks with 50-char overlap
2. **Embeddings:** Each chunk converted to 768-dim vector using `models/embedding-001`
3. **Vector Storage:** JD embeddings stored in FAISS index
4. **Similarity Search:** Resume chunks searched against JD vectors
5. **Scoring:** L2 distance converted to similarity score (0-1)
6. **Decision:** Score >= 0.80 → shortlisted, else rejected

---

## 🏗️ Architecture

```
app/
├── routes/
│   └── agent1.py              # API endpoint
├── services/
│   └── agent1/
│       ├── agent1_service.py  # Main logic
│       ├── embeddings_service.py  # Gemini embeddings
│       └── schemas.py         # Request/Response models
├── repository/
│   └── vector_repo.py         # FAISS operations
└── utils/
    └── chunks.py              # Text chunking
```

---

## ✅ Testing

**Using curl:**
```bash
curl -X POST http://localhost:8001/agent1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "jd_text": "Python developer needed",
    "resume_text": "Experienced Python engineer"
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8001/agent1/evaluate",
    json={
        "jd_text": "Python developer needed",
        "resume_text": "Experienced Python engineer"
    }
)
print(response.json())
```

---

## 🔧 Configuration

**Threshold:** Default = 0.80 (80% similarity)
- Modify in: `app/services/agent1/agent1_service.py`
- Line: `self.threshold = 0.80`

**Chunk Size:** Default = 500 characters
- Modify in: `app/utils/chunks.py`
- Function: `chunk_text(chunk_size=500)`

**Top Matches:** Default = 5
- Modify in: `app/services/agent1/agent1_service.py`
- Line: `matched_topics[:5]`

---

## 📝 Notes

- API key loaded from `.env` only (never hardcoded)
- CORS enabled for `http://localhost:3000`
- Vector DB persists to disk after each evaluation
- Stateless design: each request is independent
- No external database required for Agent 1
