# Interview Assistant - Documentation Index

## 📚 Documentation Overview

This folder contains comprehensive documentation for the Interview Assistant project.

---

## 📄 Documents

### 1. **HLD.md** - High-Level Design
**Purpose:** Complete system architecture and design decisions

**Contents:**
- System overview and architecture diagram
- Technology stack justification
- Models and APIs used (Gemini embedding-001, gemini-2.5-flash)
- Agent communication patterns
- Data flow and storage architecture
- Configuration management
- API endpoints specification
- Security considerations
- Performance optimization
- Scalability roadmap
- Dependencies justification
- Monitoring and logging strategy
- Testing approach
- Deployment considerations
- Future enhancements

**When to Read:** 
- Understanding overall system design
- Making architectural decisions
- Onboarding new team members
- Planning future features

---

### 2. **Steps_of_Execution.md** - Execution Guide
**Purpose:** Step-by-step instructions to run the system

**Contents:**
- Prerequisites and setup
- Getting Gemini API key
- Environment configuration (.env setup)
- Installing dependencies
- Verifying server is running
- Testing Agent 1 endpoint
- Verifying data persistence
- Monitoring logs
- Troubleshooting common issues
- Development workflow
- Production deployment
- Monitoring and maintenance
- Frontend integration
- Scaling considerations
- Quick reference commands
- Support checklist

**When to Read:**
- First-time setup
- Running the application
- Troubleshooting issues
- Deploying to production
- Testing endpoints

---

### 3. **Flow.md** - Agent Communication & Flow
**Purpose:** Detailed agent interactions and data flow

**Contents:**
- System architecture overview
- Agent 1 (Similarity) - Complete flow with diagrams
- Agent 2 (Scheduling) - Planned flow
- Agent 3 (Questions) - Planned flow
- Inter-agent communication patterns
- Technology choices and justification
- Request/response flow diagrams
- Error handling and fallbacks
- Performance metrics
- Conversation history structure
- Future enhancements
- Deployment architecture
- Design principles

**When to Read:**
- Understanding how agents communicate
- Debugging data flow issues
- Planning Agent 2 and Agent 3 implementation
- Understanding technology choices
- Optimizing performance

---

## 🔑 Key Information Quick Reference

### API Keys
- **Location:** `backend/.env`
- **Required:** `GOOGLE_API_KEY` (Gemini API)
- **Get from:** https://makersuite.google.com/app/apikey

### Vector Database
- **Type:** FAISS (Local)
- **Location:** `backend/data/faiss_index/`
- **Files:** `index.faiss`, `metadata.pkl`

### Embeddings Model
- **Model:** `models/embedding-001`
- **Dimension:** 768
- **Provider:** Google Gemini

### LLM Model (Planned)
- **Model:** `gemini-2.5-flash`
- **Provider:** Google Gemini

### Backend Server
- **Framework:** FastAPI
- **Port:** 8001
- **URL:** http://localhost:8001
- **Docs:** http://localhost:8001/docs

### Frontend (Planned)
- **Framework:** React
- **Port:** 3000
- **URL:** http://localhost:3000

---

## 🚀 Quick Start

### 1. Setup (First Time)
```bash
cd backend
start.bat  # Windows
# or
./start.sh  # Linux/Mac
```

### 2. Configure API Key
Edit `backend/.env`:
```env
GOOGLE_API_KEY=your_actual_key
```

### 3. Test Agent 1
```bash
curl -X POST http://localhost:8001/agent1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"jd_text":"...", "resume_text":"..."}'
```

### 4. View API Docs
Open: http://localhost:8001/docs

---

## 📊 Architecture Summary

```
Frontend (React)
    ↓ HTTP/REST
FastAPI Backend (Port 8001)
    ├─ Agent 1: JD-Resume Similarity (IMPLEMENTED)
    ├─ Agent 2: Scheduling (PLANNED)
    └─ Agent 3: Questions (PLANNED)
    ↓
External Services
    ├─ Gemini API (Embeddings + LLM)
    ├─ FAISS (Vector DB - Local)
    └─ PostgreSQL (Optional - Agent 2)
```

---

## 🔄 Agent 1 Flow (Implemented)

```
Input (JD + Resume)
    ↓
Chunking (500 chars)
    ↓
Embeddings (Gemini embedding-001)
    ↓
FAISS Vector Search (L2 distance)
    ↓
Similarity Scoring
    ↓
Decision (>= 0.80 → shortlisted)
    ↓
Output (Score + Topics + Decision)
```

---

## 📋 Technology Stack

| Component | Technology | Version | Why |
|-----------|-----------|---------|-----|
| Framework | FastAPI | 0.109.0 | Modern, async, auto-docs |
| Server | Uvicorn | 0.27.0 | Production-ready ASGI |
| Embeddings | Gemini embedding-001 | - | Free, 768-dim, semantic |
| LLM | Gemini 2.5 Flash | - | Fast, cost-effective |
| Vector DB | FAISS | 1.9.0 | Local, fast, no deps |
| Validation | Pydantic | 2.12.5 | Type-safe, auto-docs |
| Config | python-dotenv | 1.0.0 | Secure secrets |
| ORM | SQLAlchemy | 2.0.25 | For Agent 2 (DB) |
| PDF | PyPDF2 | 3.0.1 | Document parsing |

---

## 🔐 Security

- ✓ API keys in `.env` only (never hardcoded)
- ✓ CORS restricted to localhost:3000
- ✓ Pydantic input validation
- ✓ No sensitive data in error messages
- ✓ `.env` in `.gitignore`

---

## 📈 Performance

| Operation | Time |
|-----------|------|
| Text Chunking | ~10ms |
| Embedding Generation | ~500-1000ms |
| FAISS Search | ~50ms |
| Similarity Calculation | ~20ms |
| **Total Request** | **~600-1100ms** |

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
netstat -ano | findstr :8001  # Find process
taskkill /PID <PID> /F        # Kill process
```

### API Key Not Found
- Check `.env` file exists
- Verify `GOOGLE_API_KEY=` is set
- Restart server

### FAISS Import Error
```bash
pip install faiss-cpu==1.9.0.post1
```

### Gemini API Error
- Verify API key is correct
- Check API is enabled in Google Cloud
- Ensure quota not exceeded

---

## 📞 Support

For issues:
1. Check relevant documentation
2. Review error message in logs
3. Verify `.env` configuration
4. Check API key validity
5. Restart server

---

## 🎯 Next Steps

1. **Read HLD.md** - Understand system design
2. **Follow Steps_of_Execution.md** - Setup and run
3. **Read Flow.md** - Understand agent communication
4. **Test Agent 1** - Verify implementation
5. **Plan Agent 2** - Interview scheduling
6. **Plan Agent 3** - Question generation
7. **Build Frontend** - React UI

---

## 📝 Document Maintenance

- **Last Updated:** 2024-01-15
- **Version:** 1.0
- **Status:** Complete for Agent 1, Planned for Agents 2 & 3

---

## 📚 Additional Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Gemini API:** https://ai.google.dev/
- **FAISS:** https://github.com/facebookresearch/faiss
- **LangChain:** https://python.langchain.com/
- **Pydantic:** https://docs.pydantic.dev/

---

## ✅ Checklist

- [ ] Read HLD.md
- [ ] Read Steps_of_Execution.md
- [ ] Read Flow.md
- [ ] Get Gemini API key
- [ ] Configure .env
- [ ] Run start.bat
- [ ] Test Agent 1
- [ ] Verify FAISS persistence
- [ ] Access API docs
- [ ] Ready for development

---

**Interview Assistant - Comprehensive Documentation**
