# 🔐 Security Guide - Interview Assistant

> Comprehensive guide for securing your Interview Assistant project and handling sensitive information.

---

## ⚠️ CRITICAL: Exposed API Key Incident

### What Happened
Your Google Gemini API key was accidentally committed to the GitHub repository. This is a **CRITICAL SECURITY ISSUE** that requires immediate action.

### Exposed Information
- ❌ Google Gemini API Key (in `.env` file)
- ❌ PostgreSQL Database Credentials (in `.env` file)

### Immediate Actions Required
1. ✅ Rotate/Regenerate the exposed API key
2. ✅ Remove the key from git history
3. ✅ Update `.env` to use placeholder values
4. ✅ Add `.env` to `.gitignore`
5. ✅ Force push changes to remove from history

---

## 🔑 Step 1: Rotate Exposed Credentials

### Google Gemini API Key

**Steps to rotate:**
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Navigate to API Keys section
3. Delete the exposed key: `AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng`
4. Create a new API key
5. Update your local `.env` file with the new key

**Verification:**
```bash
# Test the new key
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key=YOUR_NEW_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": {"parts": [{"text": "test"}]}}'
```

### PostgreSQL Credentials

**Steps to rotate:**
1. Connect to your PostgreSQL database
2. Change the password for the `postgres` user:
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_secure_password';
   ```
3. Update `.env` with new credentials
4. Verify connection works

---

## 🔄 Step 2: Remove Secrets from Git History

### Option A: Using BFG Repo-Cleaner (Recommended)

**Installation:**
```bash
# Download BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# Or using Homebrew (macOS)
brew install bfg
```

**Remove secrets:**
```bash
# Clone a fresh copy of your repo
git clone --mirror https://github.com/yourusername/InterviewAssistant.git

# Create a file with patterns to remove
echo "AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng" > secrets.txt
echo "945725" >> secrets.txt  # PostgreSQL password

# Run BFG to remove secrets
bfg --replace-text secrets.txt InterviewAssistant.git

# Clean up
cd InterviewAssistant.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push changes
git push --force
```

### Option B: Using git-filter-branch

```bash
# WARNING: This rewrites history for all commits
# Only use if BFG is not available

# Remove .env file from all commits
git filter-branch --tree-filter 'rm -f backend/.env' -- --all

# Remove specific secrets
git filter-branch --tree-filter 'sed -i "s/AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng/REDACTED/g" backend/.env' -- --all

# Force push
git push --force --all
```

### Option C: Using git-secrets (Prevention)

**Installation:**
```bash
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
make install
```

**Setup:**
```bash
# Install hooks in your repo
cd InterviewAssistant
git secrets --install

# Add patterns to detect
git secrets --register-aws
git secrets --add 'AIzaSy[A-Za-z0-9_-]{33}'  # Gemini API key pattern
git secrets --add 'postgresql://.*:.*@'      # PostgreSQL connection string
```

**Usage:**
```bash
# Scan for secrets before committing
git secrets --scan

# Scan all commits
git secrets --scan-history
```

---

## 📝 Step 3: Environment Configuration

### Create `.env` from Template

```bash
cd backend

# Copy the template
cp .env.example .env

# Edit with your actual values
nano .env  # or use your preferred editor
```

### `.env` File Structure

```env
# 🔑 Google Gemini API Configuration
GOOGLE_API_KEY=your_new_api_key_here

# 🗄️ PostgreSQL Database
DATABASE_URL=postgresql://postgres:new_password@localhost:5432/interview_assistant

# 📦 Redis (optional)
REDIS_URL=redis://localhost:6379/0

# 🌐 CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# 🌍 Environment
ENVIRONMENT=development
```

### Verify `.env` is in `.gitignore`

```bash
# Check if .env is ignored
git check-ignore -v backend/.env

# Should output:
# .gitignore:5:.env
```

---

## 🔍 Step 4: Verify No Secrets Remain

### Scan Repository for Secrets

```bash
# Using git-secrets
git secrets --scan-history

# Using grep (basic)
grep -r "AIzaSy" .
grep -r "postgresql://" .
grep -r "password" .

# Using truffleHog (advanced)
pip install truffleHog
truffleHog filesystem . --json
```

### Check Git History

```bash
# Search git history for API key
git log -p -S "AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng"

# Search for password patterns
git log -p -S "password" | head -50
```

### Verify Commits

```bash
# Show all commits that modified .env
git log --follow -- backend/.env

# Show content of .env in latest commit
git show HEAD:backend/.env
```

---

## 🚀 Step 5: Git Commands to Secure Repository

### Complete Cleanup Workflow

```bash
# 1. Ensure .env is in .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "security: ensure .env is in .gitignore"

# 2. Remove .env from git tracking (if it was tracked)
git rm --cached backend/.env
git commit -m "security: remove .env from git tracking"

# 3. Update .env.example with placeholder values
git add backend/.env.example
git commit -m "security: update .env.example with placeholders"

# 4. Force push to remove from history (if secrets were committed)
git push --force origin main

# 5. Verify no secrets remain
git log -p | grep -i "AIzaSy" || echo "✅ No API keys found in history"
```

### For Each Team Member

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create local .env from template
cp backend/.env.example backend/.env

# 3. Add your actual API keys to .env
nano backend/.env

# 4. Verify .env is not tracked
git status | grep ".env" || echo "✅ .env is properly ignored"

# 5. Verify you can run the application
python backend/main.py
```

---

## 📋 Security Checklist

### Before Committing

- [ ] `.env` file exists locally with actual values
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` has only placeholder values
- [ ] No API keys in code files
- [ ] No passwords in code files
- [ ] No connection strings in code files
- [ ] Run `git secrets --scan` before commit

### Before Pushing

- [ ] All secrets are in `.env` (not committed)
- [ ] `.env.example` is updated with new variables
- [ ] `.gitignore` includes `.env`
- [ ] No sensitive data in commit messages
- [ ] Run `git log -p | grep -i "password"` to verify

### After Pushing

- [ ] Verify on GitHub that `.env` is not in repo
- [ ] Check git history for any exposed secrets
- [ ] Rotate any exposed credentials
- [ ] Notify team members of changes

---

## 🛡️ Best Practices

### 1. Never Hardcode Secrets

❌ **Bad:**
```python
GOOGLE_API_KEY = "AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng"
```

✅ **Good:**
```python
from app.config import settings
api_key = settings.GOOGLE_API_KEY
```

### 2. Use Environment Variables

❌ **Bad:**
```python
db_url = "postgresql://user:password@localhost:5432/db"
```

✅ **Good:**
```python
from app.config import settings
db_url = settings.DATABASE_URL
```

### 3. Use `.env.example` as Template

❌ **Bad:**
```env
GOOGLE_API_KEY=AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng
```

✅ **Good:**
```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

### 4. Rotate Credentials Regularly

- Rotate API keys every 90 days
- Rotate database passwords every 90 days
- Immediately rotate if exposed
- Use different keys for different environments

### 5. Use Secrets Management Tools

**For Development:**
- Use `.env` files with `python-dotenv`
- Use `git-secrets` to prevent commits

**For Production:**
- Use AWS Secrets Manager
- Use HashiCorp Vault
- Use Azure Key Vault
- Use Google Cloud Secret Manager

### 6. Implement Access Controls

- Limit API key permissions to minimum required
- Use separate keys for different services
- Use separate keys for different environments
- Audit API key usage regularly

---

## 🔔 Monitoring & Alerts

### GitHub Secret Scanning

1. Go to repository Settings
2. Enable "Secret scanning"
3. Enable "Push protection"
4. GitHub will alert on exposed secrets

### Third-Party Services

**TruffleHog:**
```bash
pip install truffleHog
truffleHog filesystem . --json > secrets_report.json
```

**GitGuardian:**
- Sign up at https://www.gitguardian.com/
- Connect your GitHub repository
- Receive alerts for exposed secrets

---

## 📚 Resources

### Documentation
- [Google Gemini API Security](https://ai.google.dev/docs)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)

### Tools
- [git-secrets](https://github.com/awslabs/git-secrets)
- [TruffleHog](https://github.com/trufflesecurity/truffleHog)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitGuardian](https://www.gitguardian.com/)

### Articles
- [How to Remove Secrets from Git History](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Secrets Management Best Practices](https://www.gitguardian.com/blog/secrets-management-best-practices)

---

## 🆘 Emergency Response

### If Secrets Are Exposed

1. **Immediately rotate credentials**
   ```bash
   # Regenerate API keys
   # Change database passwords
   # Update all services
   ```

2. **Remove from git history**
   ```bash
   # Use BFG or git-filter-branch
   # Force push changes
   ```

3. **Notify team members**
   - Send urgent notification
   - Provide new credentials securely
   - Update documentation

4. **Monitor for abuse**
   - Check API usage logs
   - Monitor database access logs
   - Set up alerts for unusual activity

5. **Document incident**
   - Record what happened
   - Record when it was discovered
   - Record remediation steps
   - Update security procedures

---

## ✅ Verification Checklist

After implementing security measures:

- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` has placeholder values
- [ ] No secrets in git history
- [ ] All team members have `.env` setup
- [ ] API keys are rotated
- [ ] Database passwords are changed
- [ ] git-secrets is installed and configured
- [ ] GitHub secret scanning is enabled
- [ ] All tests pass with new credentials
- [ ] Documentation is updated

---

## 📞 Support

For security issues:
1. Do NOT create public issues
2. Email security team privately
3. Include detailed information
4. Allow time for response

---

**Last Updated:** January 2024
**Version:** 1.0.0
**Status:** Critical Security Guide
