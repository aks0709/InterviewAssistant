# 🚨 URGENT: FIX EXPOSED .env FILE

## ⚠️ PROBLEM

Your `backend/.env` file with **EXPOSED SECRETS** is in git history:
- Google API Key: `AQ.Ab8RN6J854Ax4WQB9-qMQ2GjtSoqfiBKYRz1YzbXqfUqPHa4Gw`
- PostgreSQL Password: `945725`

---

## ✅ SOLUTION (3 SIMPLE STEPS)

### STEP 1: Rotate Your Credentials (5 minutes)

```bash
# 1. Go to: https://ai.google.dev/
# Delete the exposed key: AQ.Ab8RN6J854Ax4WQB9-qMQ2GjtSoqfiBKYRz1YzbXqfUqPHa4Gw
# Create a NEW API key and copy it

# 2. Change PostgreSQL password:
# ALTER USER postgres WITH PASSWORD 'new_secure_password';

# 3. Update your local .env file
cd backend
nano .env
# Update:
# GOOGLE_API_KEY=your_new_key_here
# DATABASE_URL=postgresql://postgres:new_password@localhost:5432/interview_assistant
```

### STEP 2: Remove from Git History (10 minutes)

```bash
# Install BFG (if not installed)
brew install bfg  # macOS
# Windows: Download from https://rtyley.github.io/bfg-repo-cleaner/

# Go to parent directory
cd c:\Users\akum1183\OneDrive - Capgemini\Desktop

# Clone mirror
git clone --mirror https://github.com/yourusername/InterviewAssistant.git InterviewAssistant.git
cd InterviewAssistant.git

# Create secrets file
echo AQ.Ab8RN6J854Ax4WQB9-qMQ2GjtSoqfiBKYRz1YzbXqfUqPHa4Gw > secrets.txt
echo 945725 >> secrets.txt

# Run BFG
bfg --replace-text secrets.txt

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push back
git push --force

# Cleanup
cd ..
rmdir /s InterviewAssistant.git
del secrets.txt
```

### STEP 3: Verify & Commit (5 minutes)

```bash
cd InterviewAssistant

# Verify secrets are gone
git log -p | findstr "AQ.Ab8RN6J854Ax4WQB9" || echo ✅ API key removed
git log -p | findstr "945725" || echo ✅ Password removed

# Commit security files
git add .gitignore README.md backend\.env.example docs\*.md *.md
git commit -m "security: remove exposed credentials and add security measures"
git push origin main
```

---

## 📋 CHECKLIST

- [ ] Rotated Google API key
- [ ] Changed PostgreSQL password
- [ ] Updated local .env file
- [ ] Ran BFG to remove from history
- [ ] Verified secrets are gone
- [ ] Committed security files
- [ ] Pushed to GitHub

---

## ✅ AFTER THIS IS DONE

1. Tell your team to pull latest changes
2. They create .env from .env.example
3. You send them new credentials separately
4. Everyone verifies .env is ignored: `git status | grep .env` (should show nothing)

---

**Time Required:** 20-30 minutes
**Risk Level:** Low
**Status:** Ready to execute

Start with STEP 1 now! 🚀
