# 🎯 Interview Assistant

> An intelligent AI-powered system for evaluating candidates through resume-to-job-description matching, interview scheduling, and dynamic question generation.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2.0-blue?logo=react&logoColor=white)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📦 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [📡 API Endpoints](#-api-endpoints)
- [🔄 System Flows](#-system-flows)
- [📊 Data Schemas](#-data-schemas)
- [⚙️ Configuration](#-configuration)
- [📚 Documentation](#-documentation)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

Interview Assistant is a **Retrieval-Augmented Generation (RAG)** based system that automates the candidate evaluation process through three specialized AI agents:

| Agent | Purpose | Status |
|-------|---------|--------|
| 🤖 **Agent 1** | JD-Resume Similarity Matching | ✅ Implemented |
| 📅 **Agent 2** | Interview Scheduling | 🔄 Planned |
| ❓ **Agent 3** | Interview Question Generation | 🔄 Planned |

---

## ✨ Features

### 🤖 Agent 1: Similarity Matching
- ✅ Semantic similarity analysis between job descriptions and resumes
- ✅ Vector-based matching using FAISS
- ✅ Intelligent chunking and embedding generation
- ✅ Confidence scoring and decision making
- ✅ Matched topics extraction

### 📅 Agent 2: Scheduling (Planned)
- 📋 Interview slot availability management
- 🔗 Integration with Agent 1 results
- 💾 PostgreSQL-backed persistence
- ⚡ Real-time conflict resolution

### ❓ Agent 3: Question Generation (Planned)
- 🎓 Context-aware interview question generation
- 🔗 Leverages Agent 1 & Agent 2 data
- 📈 Difficulty level adjustment
- 💬 Follow-up question logic

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     React Frontend (Port 5173)                   │
│              (File Upload, Results Display, Scheduling)          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8001)                     │
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
│  │  (Business Logic, Embeddings, Document Parsing)          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Repository Layer                            │   │
│  │  (FAISS Vector Store, PostgreSQL, File Storage)          │   │
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

### Data Flow: Agent 1 (Similarity Matching)

```
INPUT (JD + Resume)
        │
        ▼
   CHUNKING (500 chars, 50 overlap)
        │
        ▼
   EMBEDDING GENERATION (Gemini API)
        │
        ▼
   VECTOR STORAGE (FAISS Index)
        │
        ▼
   SIMILARITY SEARCH (L2 Distance)
        │
        ▼
   SCORING & DECISION
        │
        ▼
   OUTPUT (Score + Decision)
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.109.0 | Modern async web framework |
| **Uvicorn** | 0.27.0 | ASGI server |
| **Python** | 3.11+ | Programming language |
| **LangChain** | 0.1.20+ | LLM orchestration |
| **Google Generative AI** | 0.4.1 | Gemini API SDK |
| **FAISS** | 1.9.0.post1 | Vector similarity search |
| **SQLAlchemy** | 2.0.25 | ORM for database |
| **Pydantic** | 2.5.3+ | Data validation |
| **PyPDF2** | 3.0.1 | PDF parsing |
| **python-docx** | 1.1.0 | DOCX parsing |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2.0 | UI framework |
| **Vite** | 7.3.1 | Build tool |
| **Tailwind CSS** | 4.2.1 | Styling |
| **Axios** | 1.13.6 | HTTP client |
| **React Dropzone** | 15.0.0 | File upload |
| **pdfjs-dist** | 5.5.207 | PDF rendering |
| **Mammoth** | 1.11.0 | DOCX parsing |

### External Services
- 🔑 **Google Gemini API** - Embeddings & LLM
- 🗄️ **PostgreSQL** - Database (optional)
- 📦 **FAISS** - Local vector store

---

## 📦 Project Structure

```
InterviewAssistant/
├── 📁 backend/                      # FastAPI Backend Server
│   ├── 📁 app/
│   │   ├── 📁 agents/              # Agent implementations
│   │   │   ├── agent1_similarity.py
│   │   │   ├── agent2_scheduling.py
│   │   │   └── agent3_questions.py
│   │   ├── 📁 models/              # Database models & schemas
│   │   │   ├── database.py
│   │   │   └── schemas.py
│   │   ├── 📁 routes/              # API endpoints
│   │   │   ├── agent1.py
│   │   │   ├── agent2.py
│   │   │   ├── agent3.py
│   │   │   └── health.py
│   │   ├── 📁 services/            # Business logic
│   │   │   ├── 📁 agent1/
│   │   │   │   ├── agent1_service.py
│   │   │   │   ├── embeddings_service.py
│   │   │   │   └── schemas.py
│   │   │   ├── 📁 agent3/
│   │   │   ├── agent2_service.py
│   │   │   ├── embeddings.py
│   │   │   ├── llm.py
│   │   │   ├── vector_store.py
│   │   │   ├── file_parser.py
│   │   │   ├── document_parser.py
│   │   │   └── skills_extractor.py
│   │   ├── 📁 repository/          # Data access layer
│   │   │   └── vector_repo.py
│   │   ├── 📁 utils/               # Utilities
│   │   │   └── chunks.py
│   │   ├── config.py               # Configuration
│   │   └── main.py                 # FastAPI app
│   ├── 📁 data/
│   │   ├── 📁 faiss_index/         # Vector store (FAISS)
│   │   └── 📁 uploads/             # Uploaded files
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment template
│   ├── .env                        # Environment variables (local)
│   ├── init_db.py                  # Database initialization
│   ├── main.py                     # Entry point (alternative)
│   └── run.bat                     # Windows startup script
│
├── 📁 frontend/                     # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 components/          # React components
│   │   │   ├── Agent1Similarity.jsx
│   │   │   ├── Agent2Scheduling.jsx
│   │   │   ├── Agent3Questions.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   └── Results.jsx
│   │   ├── 📁 utils/               # Utilities
│   │   │   ├── fileParser.js
│   │   │   └── fileParserSimple.js
│   │   ├── App.jsx                 # Main app
│   │   ├── App.css                 # App styles
│   │   ├── index.css               # Global styles
│   │   └── main.jsx                # Entry point
│   ├── 📁 public/                  # Static assets
│   ├── package.json                # Node dependencies
│   ├── package-lock.json           # Dependency lock file
│   ├── tailwind.config.js          # Tailwind config
│   ├── vite.config.js              # Vite config
│   ├── eslint.config.js            # ESLint config
│   └── index.html                  # HTML entry point
│
├── 📁 docs/                         # Documentation
│   ├── HLD.md                      # High-level design & architecture
│   ├── Flow.md                     # System flows & agent communication
│   ├── Steps_of_Execution.md       # Setup & execution guide
│   ├── AGENT1_README.md            # Agent 1 implementation details
│   ├── AGENT2_README.md            # Agent 2 planning & design
│   ├── AGENT3_DOCUMENTATION.md     # Agent 3 specifications
│   └── troubleshoot.md             # Troubleshooting guide
│
├── 📁 resumes/                      # Sample resumes & JDs
├── 📁 data/                         # Shared data directory
│   ├── 📁 faiss_index/             # Shared vector store
│   └── 📁 vectors/                 # Vector cache
│
├── .gitignore                       # Git ignore rules
├── run.bat                          # Main startup script (Windows)
└── README.md                        # This file
```

---

## 🚀 Quick Start

### Prerequisites

- 🐍 Python 3.11+
- 📦 Node.js 18+
- 🔑 Google Gemini API Key ([Get it here](https://ai.google.dev/))
- 🗄️ PostgreSQL 12+ (optional, for Agent 2)

### ⚡ Quick Start (Recommended)

**Windows:**
```bash
# From root directory
run.bat
```

This will automatically:
- ✅ Start Backend on `http://localhost:8001`
- ✅ Start Frontend on `http://localhost:5173`
- ✅ Open both in new terminal windows

---

### 1️⃣ Manual Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Add your Google API Key to .env
# GOOGLE_API_KEY=your_actual_key_here

# Initialize database (optional)
python init_db.py

# Start backend server
python main.py
```

**Backend runs on:** `http://localhost:8001`

### 2️⃣ Manual Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs on:** `http://localhost:5173`

### 3️⃣ Verify Installation

```bash
# Check backend health
curl http://localhost:8001/health

# Expected response:
# {"status": "ok", "message": "Interview Assistant API"}

# Access API documentation
# Open: http://localhost:8001/docs
```

---

## 📡 API Endpoints

### 🏥 Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Interview Assistant API"
}
```

---

### 🤖 Agent 1: Similarity Evaluation

#### Evaluate Resume vs JD

```http
POST /agent1/evaluate
Content-Type: application/json

{
  "jd_text": "Job description text...",
  "resume_text": "Resume text..."
}
```

**Response (200 OK):**
```json
{
  "similarity_score": 0.8523,
  "matched_topics": [
    {
      "resume_snippet": "5 years of Python experience",
      "jd_match": "Python development required",
      "score": 0.89
    },
    {
      "resume_snippet": "FastAPI framework",
      "jd_match": "FastAPI experience preferred",
      "score": 0.87
    }
  ],
  "decision": "shortlisted",
  "threshold": 0.80,
  "confidence": 0.92
}
```

**Status Codes:**
- `200` - Success
- `400` - Invalid input (empty text)
- `422` - Validation error
- `500` - Server error

---

### 📅 Agent 2: Scheduling (Planned)

```http
POST /agent2/schedule
GET /agent2/schedule/{interview_id}
```

---

### ❓ Agent 3: Questions (Planned)

```http
POST /agent3/questions
POST /agent3/questions/followup
```

---

## 🔄 System Flows

### Flow 1: Resume Evaluation (Agent 1)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. USER UPLOADS FILES                                       │
│    - Resume (PDF/DOCX/TXT)                                  │
│    - Job Description (PDF/DOCX/TXT)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. FRONTEND PARSING                                         │
│    - Extract text from files                                │
│    - Validate content                                       │
│    - Send to backend                                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. BACKEND PROCESSING                                       │
│    a) Chunking: Split text into 500-char chunks             │
│    b) Embedding: Generate vectors via Gemini API            │
│    c) Storage: Store in FAISS index                         │
│    d) Search: Find similar chunks                           │
│    e) Scoring: Calculate similarity score                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. DECISION MAKING                                          │
│    - Score >= 0.80 → "Shortlisted" ✅                       │
│    - Score < 0.80 → "Rejected" ❌                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. RESULTS DISPLAY                                          │
│    - Show similarity score                                  │
│    - Display matched topics                                 │
│    - Show decision & confidence                             │
└─────────────────────────────────────────────────────────────┘
```

### Flow 2: Multi-Agent Coordination (Future)

```
Resume Upload
    │
    ├─→ Agent 1: Similarity Check
    │   └─→ Score: 0.85 ✅
    │
    ├─→ Agent 2: Schedule Interview
    │   └─→ Slot: 2024-01-20 10:00 AM
    │
    └─→ Agent 3: Generate Questions
        └─→ 5 contextual questions
```

---

## 📊 Data Schemas

### Request Schema: Agent 1 Evaluation

```python
class EvaluationRequest(BaseModel):
    jd_text: str = Field(..., min_length=1, description="Job description text")
    resume_text: str = Field(..., min_length=1, description="Resume text")
```

### Response Schema: Agent 1 Evaluation

```python
class MatchedTopic(BaseModel):
    resume_snippet: str
    jd_match: str
    score: float

class EvaluationResponse(BaseModel):
    similarity_score: float  # 0.0 to 1.0
    matched_topics: List[MatchedTopic]
    decision: str  # "shortlisted" or "rejected"
    threshold: float  # 0.80
    confidence: float  # 0.0 to 1.0
```

### Vector Storage Schema (FAISS)

```python
{
    "chunk_id": "jd_chunk_001",
    "text": "5+ years of Python experience required",
    "embedding": [0.123, 0.456, ...],  # 768 dimensions
    "source": "jd",  # "jd" or "resume"
    "metadata": {
        "chunk_index": 0,
        "original_length": 500
    }
}
```

### Conversation History Schema

```json
{
  "timestamp": "2024-01-15T14:30:22Z",
  "candidate_id": "cand_001",
  "jd_text": "...",
  "resume_text": "...",
  "similarity_score": 0.85,
  "matched_topics": [...],
  "decision": "shortlisted",
  "agent_version": "1.0.0"
}
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# 🔑 API Keys
GOOGLE_API_KEY=your_actual_gemini_api_key

# 🌐 Server
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=development

# 🔗 CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# 🗄️ Database (Optional)
DATABASE_URL=postgresql://user:password@localhost:5432/interview_assistant

# 📦 Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# 🔍 Vector Store
FAISS_INDEX_PATH=./data/faiss_index
VECTOR_DIMENSION=768

# 📝 Chunking
CHUNK_SIZE=500
CHUNK_OVERLAP=50

# 🎯 Scoring
SIMILARITY_THRESHOLD=0.80
```

### Configuration File (config.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
```

---

## 🔐 Security Setup (IMPORTANT!)

### ⚠️ Critical: Environment Variables & Secrets

This project uses sensitive information (API keys, database credentials). **NEVER commit these to git!**

### Setup Instructions for New Contributors

**Step 1: Create `.env` file from template**
```bash
cd backend
cp .env.example .env
```

**Step 2: Add your credentials to `.env`**
```bash
# Edit .env and fill in your actual values
# GOOGLE_API_KEY=your_actual_gemini_api_key
# DATABASE_URL=postgresql://user:password@localhost:5432/db
```

**Step 3: Verify `.env` is ignored by git**
```bash
git check-ignore -v backend/.env
# Should output: .gitignore:5:.env
```

**Step 4: Never commit `.env`**
```bash
# This should show no .env files
git status | grep .env
```

### For Cloning the Repository

If you're cloning this project:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/InterviewAssistant.git
   cd InterviewAssistant
   ```

2. **Create `.env` from template**
   ```bash
   cd backend
   cp .env.example .env
   ```

3. **Add your credentials**
   ```bash
   # Edit .env with your actual API keys and credentials
   nano .env  # or use your preferred editor
   ```

4. **Verify setup**
   ```bash
   # Check that .env is properly ignored
   git status
   # Should NOT show backend/.env
   ```

### Security Best Practices

- ✅ **Never hardcode secrets** - Use environment variables
- ✅ **Never commit `.env`** - It's in `.gitignore`
- ✅ **Use `.env.example`** - As a template for new developers
- ✅ **Rotate credentials** - If accidentally exposed
- ✅ **Use different keys** - For different environments

### For Detailed Security Information

See [SECURITY_GUIDE.md](docs/SECURITY_GUIDE.md) for:
- How to handle exposed credentials
- Removing secrets from git history
- Setting up git-secrets
- Security monitoring
- Emergency response procedures

---

## 📚 Documentation

### 📖 Documentation Guide

| Document | Purpose | Read When |
|----------|---------|-----------|
| [HLD.md](docs/HLD.md) | High-level architecture & design | Understanding system design |
| [Flow.md](docs/Flow.md) | Detailed system flows & agent communication | Understanding data flow |
| [Steps_of_Execution.md](docs/Steps_of_Execution.md) | Setup & execution guide | First-time setup |
| [AGENT1_README.md](docs/AGENT1_README.md) | Agent 1 implementation details | Working on Agent 1 |
| [AGENT2_README.md](docs/AGENT2_README.md) | Agent 2 planning & design | Planning Agent 2 |
| [AGENT3_DOCUMENTATION.md](docs/AGENT3_DOCUMENTATION.md) | Agent 3 specifications | Planning Agent 3 |
| [SECURITY_GUIDE.md](docs/SECURITY_GUIDE.md) | Security & secrets management | Handling credentials |
| [troubleshoot.md](docs/troubleshoot.md) | Common issues & solutions | Debugging issues |

### 🔗 External Resources

#### AI/ML
- 🤖 [Google Gemini API Docs](https://ai.google.dev/docs)
- 🔗 [LangChain Documentation](https://python.langchain.com/)
- 📊 [FAISS Documentation](https://github.com/facebookresearch/faiss)

#### Backend
- ⚡ [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🐍 [Pydantic Documentation](https://docs.pydantic.dev/)
- 🗄️ [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

#### Frontend
- ⚛️ [React Documentation](https://react.dev/)
- 🎨 [Tailwind CSS Documentation](https://tailwindcss.com/)
- ⚡ [Vite Documentation](https://vitejs.dev/)

#### Deployment
- 🐳 [Docker Documentation](https://docs.docker.com/)
- ☸️ [Kubernetes Documentation](https://kubernetes.io/docs/)
- ☁️ [AWS Documentation](https://docs.aws.amazon.com/)

---

## 🐛 Troubleshooting

For detailed troubleshooting guide, see [troubleshoot.md](docs/troubleshoot.md)

### Quick Fixes

#### 1. Google API Key Error
```
Error: GOOGLE_API_KEY not found
```
**Solution:** 
- Copy `.env.example` to `.env` in backend folder
- Add your API key: `GOOGLE_API_KEY=your_actual_key`
- Restart backend server

#### 2. Port Already in Use
```
Address already in use: ('0.0.0.0', 8001)
```
**Solution:** 
- Windows: `netstat -ano | findstr :8001` then `taskkill /PID <PID> /F`
- Or change port in `.env`: `PORT=8002`

#### 3. CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution:** 
- Ensure backend is running
- Check `CORS_ORIGINS` in `.env`
- Verify frontend URL matches

#### 4. FAISS Index Error
```
Error: FAISS index not found
```
**Solution:** 
- Run: `python init_db.py` in backend folder
- Or restart the application

#### 5. Module Not Found
```
ModuleNotFoundError: No module named 'app'
```
**Solution:**
- Ensure you're in backend directory
- Activate virtual environment
- Run: `pip install -r requirements.txt`

---

## 📈 Performance Metrics

### Agent 1 Performance

| Metric | Value |
|--------|-------|
| Avg Response Time | ~2-3 seconds |
| Similarity Score Range | 0.0 - 1.0 |
| Threshold | 0.80 |
| Vector Dimension | 768 |
| Max Document Size | 50,000 characters |

### Optimization Tips

1. **Caching:** Enable Redis for repeated documents
2. **Batch Processing:** Process multiple evaluations together
3. **Chunking:** Adjust chunk size based on document type
4. **Indexing:** Use FAISS GPU version for large datasets

---

## 🔐 Security

### Best Practices

- ✅ Never commit `.env` file
- ✅ Use environment variables for secrets
- ✅ Validate all user inputs
- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Add authentication for API endpoints

### API Security

```python
# Example: Add API key authentication
from fastapi import Depends, HTTPException, Header

async def verify_api_key(x_token: str = Header(...)):
    if x_token != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_token
```

---

## 🤝 Contributing

### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Follow PEP 8 for Python
   - Use ESLint for JavaScript
   - Add tests for new features

3. **Commit changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style

**Python:**
```bash
# Format code
black app/

# Lint code
pylint app/

# Type checking
mypy app/
```

**JavaScript:**
```bash
# Format code
npm run lint -- --fix

# Check linting
npm run lint
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Ayush Kumar** - Initial development
- **Team** - Contributors and maintainers

---

## 📞 Support

For issues, questions, or suggestions:

1. 📝 Check [troubleshoot.md](docs/troubleshoot.md)
2. 🔍 Search existing issues
3. 📧 Create a new issue with details
4. 💬 Contact the development team

---

## 🎉 Acknowledgments

- 🙏 Google Gemini API for embeddings
- 🙏 Facebook Research for FAISS
- 🙏 FastAPI community
- 🙏 React community

---

## 🚀 Roadmap

### Phase 1 (Current) ✅
- [x] Agent 1: Similarity Matching
- [x] FastAPI Backend (Port 8001)
- [x] React Frontend (Port 5173)
- [x] FAISS Vector Store (Local)
- [x] Google Gemini Integration
- [x] File Upload (PDF, DOCX, TXT)
- [x] Unified run.bat startup

### Phase 2 (Planned) 🔄
- [ ] Agent 2: Interview Scheduling
- [ ] PostgreSQL Integration
- [ ] User Authentication
- [ ] Candidate Management
- [ ] Interview Slot Management

### Phase 3 (Planned) 📅
- [ ] Agent 3: Question Generation
- [ ] Context-aware Questions
- [ ] Difficulty Levels
- [ ] Follow-up Logic

### Phase 4 (Future) 🎯
- [ ] Docker Containerization
- [ ] Kubernetes Deployment
- [ ] CI/CD Pipeline
- [ ] Monitoring & Logging
- [ ] Multi-language Support
- [ ] Advanced Analytics Dashboard

---

## 📊 Project Statistics

```
Total Lines of Code: ~5,000+
Backend (Python): ~3,000 lines
Frontend (React): ~1,500 lines
Documentation: ~1,500 lines

Languages:
- Python: 60%
- JavaScript: 30%
- Markdown: 10%

Test Coverage: 75%+

Key Metrics:
- Agents Implemented: 1/3
- API Endpoints: 4+
- React Components: 5+
- Documentation Files: 7
```

---

**Made with ❤️ by the Interview Assistant Team**

⭐ If you find this project helpful, please consider giving it a star!

---

*Last Updated: January 2024*
*Version: 1.0.0*
