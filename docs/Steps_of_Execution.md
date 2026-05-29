# Interview Assistant - Steps of Execution

## Prerequisites

- Python 3.11+
- Windows (for .bat scripts) or Linux/Mac (modify scripts)
- Gemini API Key
- ~500MB disk space

---

## Step 1: Clone/Setup Project

```bash
# Navigate to project
cd InterviewAssistant

# Verify structure
dir  # Windows
ls   # Linux/Mac
```

**Expected Structure:**
```
InterviewAssistant/
├── backend/
│   ├── app/
│   ├── data/
│   ├── .env.example
│   ├── requirements.txt
│   ├── start.bat
│   └── run.bat
├── docs/
└── README.md
```

---

## Step 2: Get Gemini API Key

### 2.1 Create Google Account
- Visit: https://accounts.google.com
- Create or login to existing account

### 2.2 Get API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the generated key
4. Keep it safe (don't share)

### 2.3 Enable Gemini API
1. Go to: https://console.cloud.google.com
2. Create new project (or select existing)
3. Enable "Generative Language API"
4. Create API key from credentials

---

## Step 3: Configure Environment

### 3.1 Copy .env Template
```bash
cd backend
copy .env.example .env  # Windows
# or
cp .env.example .env    # Linux/Mac
```

### 3.2 Edit .env File
```env
# backend/.env

# REQUIRED: Your Gemini API Key
GOOGLE_API_KEY=your_actual_gemini_api_key_here

# OPTIONAL: Database (for Agent 2)
DATABASE_URL=postgresql://user:password@localhost:5432/interview_assistant

# OPTIONAL: Redis
REDIS_URL=redis://localhost:6379/0

# CORS: Frontend origin
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
```

**⚠️ IMPORTANT:**
- Never commit `.env` to git
- `.env` is in `.gitignore`
- Each developer needs their own API key

---

## Step 4: Install Dependencies

### 4.1 First Time Setup (Creates venv + installs)
```bash
cd backend
start.bat  # Windows
# or
./start.sh  # Linux/Mac (create this script)
```

**What happens:**
1. Creates `venv/` directory
2. Activates virtual environment
3. Installs all packages from `requirements.txt`
4. Starts FastAPI server

### 4.2 Subsequent Runs (Just start server)
```bash
cd backend
run.bat  # Windows
# or
./run.sh  # Linux/Mac
```

**Output:**
```
========================================
Interview Assistant Backend Setup
========================================

Creating virtual environment...
Virtual environment created successfully!

Activating virtual environment...

Installing dependencies...
Successfully installed 50+ packages...

========================================
Starting FastAPI Backend Server...
========================================
Server will run at: http://localhost:8001
API Docs available at: http://localhost:8001/docs
```

---

## Step 5: Verify Server is Running

### 5.1 Check Health Endpoint
```bash
# In another terminal
curl http://localhost:8001/
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "Interview Assistant API"
}
```

### 5.2 Access API Documentation
- Open browser: `http://localhost:8001/docs`
- See all available endpoints
- Test endpoints interactively

---

## Step 6: Test Agent 1 Endpoint

### 6.1 Using curl
```bash
curl -X POST http://localhost:8001/agent1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "jd_text": "We are looking for a Python developer with 3+ years experience in FastAPI and machine learning.",
    "resume_text": "Software Engineer with 5 years Python experience. Built FastAPI applications and ML models using scikit-learn."
  }'
```

### 6.2 Using Python
```python
import requests

response = requests.post(
    "http://localhost:8001/agent1/evaluate",
    json={
        "jd_text": "Python developer with FastAPI experience needed",
        "resume_text": "5 years Python, FastAPI, ML experience"
    }
)

print(response.json())
```

### 6.3 Using Postman
1. Open Postman
2. Create new POST request
3. URL: `http://localhost:8001/agent1/evaluate`
4. Body (JSON):
```json
{
  "jd_text": "Your JD here",
  "resume_text": "Your resume here"
}
```
5. Send

### 6.4 Expected Response
```json
{
  "similarity_score": 0.8523,
  "matched_topics": [
    {
      "resume_snippet": "5 years Python experience...",
      "jd_match": "Python developer with...",
      "score": 0.89
    }
  ],
  "decision": "shortlisted",
  "threshold": 0.80
}
```

---

## Step 7: Verify Data Persistence

### 7.1 Check FAISS Index
```bash
# After running Agent 1, check:
backend/data/faiss_index/
├── index.faiss      # Vector index
└── metadata.pkl     # Metadata
```

### 7.2 Check History (Optional)
```bash
# If history saving is enabled:
backend/data/history/
├── 2024-01-15_143022_shortlisted.json
└── 2024-01-15_143045_rejected.json
```

---

## Step 8: Monitor Logs

### 8.1 Server Logs
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
INFO:     POST /agent1/evaluate
INFO:     Completed request
```

### 8.2 Error Logs
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  ...
```

---

## Step 9: Troubleshooting

### Issue: Port 8001 Already in Use
```bash
# Find process using port 8001
netstat -ano | findstr :8001  # Windows
lsof -i :8001                 # Linux/Mac

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac
```

### Issue: API Key Not Found
```
ERROR: GOOGLE_API_KEY not found in .env
```

**Solution:**
1. Check `.env` file exists
2. Verify `GOOGLE_API_KEY=` is set
3. Restart server

### Issue: FAISS Import Error
```
ModuleNotFoundError: No module named 'faiss'
```

**Solution:**
```bash
cd backend
venv\Scripts\activate  # Windows
pip install faiss-cpu==1.9.0.post1
```

### Issue: Gemini API Error
```
Error: Invalid API key
```

**Solution:**
1. Verify API key is correct
2. Check API is enabled in Google Cloud
3. Ensure quota not exceeded

---

## Step 10: Development Workflow

### 10.1 Make Code Changes
```bash
# Edit files in app/
# Changes auto-reload due to --reload flag
```

### 10.2 Test Changes
```bash
# Server auto-reloads
# Test endpoint again
curl http://localhost:8001/agent1/evaluate ...
```

### 10.3 Check Logs
```bash
# Watch server output for errors
# Fix and save file
# Server reloads automatically
```

---

## Step 11: Production Deployment

### 11.1 Environment Setup
```bash
# Set production environment
ENVIRONMENT=production
GOOGLE_API_KEY=<production_key>
DATABASE_URL=<production_db>
```

### 11.2 Run with Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### 11.3 Docker Deployment (Optional)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## Step 12: Monitoring & Maintenance

### 12.1 Check Server Health
```bash
# Every 5 minutes
curl http://localhost:8001/
```

### 12.2 Monitor Disk Usage
```bash
# Check FAISS index size
du -sh backend/data/faiss_index/  # Linux/Mac
dir backend\data\faiss_index\     # Windows
```

### 12.3 Clear Old History (Optional)
```bash
# Remove old evaluation files
rm backend/data/history/*.json
```

---

## Step 13: Integration with Frontend

### 13.1 Frontend Setup (When Ready)
```bash
# In separate terminal
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

### 13.2 API Calls from Frontend
```javascript
// React example
const response = await fetch('http://localhost:8001/agent1/evaluate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jd_text: jdText,
    resume_text: resumeText
  })
});

const data = await response.json();
console.log(data.decision);  // "shortlisted" or "rejected"
```

---

## Step 14: Scaling Considerations

### 14.1 Multiple Requests
- Current: Sequential processing
- Future: Async queue with Celery

### 14.2 Large Documents
- Current: 500-char chunks
- Optimize: Adjust chunk size based on document

### 14.3 API Rate Limiting
- Current: No limit
- Future: Implement rate limiting

---

## Quick Reference

### Start Server
```bash
cd backend && run.bat
```

### Test Agent 1
```bash
curl -X POST http://localhost:8001/agent1/evaluate \
  -H "Content-Type: application/json" \
  -d '{"jd_text":"...", "resume_text":"..."}'
```

### View API Docs
```
http://localhost:8001/docs
```

### Check Logs
```bash
# Watch server output in terminal
```

### Stop Server
```bash
Ctrl+C  # In terminal running server
```

---

## Checklist

- [ ] Python 3.11+ installed
- [ ] Gemini API key obtained
- [ ] `.env` file configured
- [ ] `start.bat` executed successfully
- [ ] Server running on port 8001
- [ ] Health endpoint responds
- [ ] Agent 1 endpoint tested
- [ ] FAISS index created
- [ ] API docs accessible
- [ ] Ready for frontend integration

---

## Support

For issues:
1. Check logs in terminal
2. Review error message
3. Check `.env` configuration
4. Verify API key validity
5. Restart server

---

## Next Steps

1. **Implement Agent 2** - Interview Scheduling
2. **Implement Agent 3** - Question Generation
3. **Build Frontend** - React UI
4. **Add Authentication** - User management
5. **Deploy** - Production environment
