# 🔐 Git Security Commands - Interview Assistant

> Complete guide with all git commands needed to secure your repository after accidental secret exposure.

---

## ⚠️ Situation Summary

Your Google Gemini API key and PostgreSQL credentials were accidentally committed to GitHub in the `.env` file.

**Exposed Information:**
- ❌ Google Gemini API Key: `AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng`
- ❌ PostgreSQL Password: `945725`
- ❌ Database URL: `postgresql://postgres:945725@localhost:5432/interview_assistant`

---

## 🚨 Immediate Actions (Do This First!)

### Step 1: Rotate All Exposed Credentials

```bash
# 1. Regenerate Google Gemini API Key
# Go to: https://ai.google.dev/
# Delete the exposed key
# Create a new key

# 2. Change PostgreSQL Password
# Connect to your database and run:
# ALTER USER postgres WITH PASSWORD 'new_secure_password';

# 3. Update your local .env file with new credentials
nano backend/.env
```

### Step 2: Ensure .env is in .gitignore

```bash
# Verify .env is in .gitignore
cat .gitignore | grep ".env"

# Should output:
# .env
# .env.local
# .env.*.local

# If not present, add it:
echo ".env" >> .gitignore
git add .gitignore
git commit -m "security: ensure .env is in .gitignore"
```

---

## 🔄 Remove Secrets from Git History

### Option A: Using BFG Repo-Cleaner (RECOMMENDED)

**Installation:**
```bash
# macOS
brew install bfg

# Windows (using Chocolatey)
choco install bfg

# Or download from: https://rtyley.github.io/bfg-repo-cleaner/
```

**Remove secrets from history:**
```bash
# 1. Create a mirror clone
git clone --mirror https://github.com/yourusername/InterviewAssistant.git
cd InterviewAssistant.git

# 2. Create a file with secrets to remove
cat > secrets.txt << EOF
AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng
945725
postgresql://postgres:945725@localhost:5432/interview_assistant
EOF

# 3. Run BFG to remove secrets
bfg --replace-text secrets.txt

# 4. Clean up git history
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Push changes back
git push --force

# 6. Clean up
cd ..
rm -rf InterviewAssistant.git
rm secrets.txt
```

### Option B: Using git-filter-branch

```bash
# WARNING: This rewrites all history
# Only use if BFG is not available

# 1. Remove .env file from all commits
git filter-branch --tree-filter 'rm -f backend/.env' -- --all

# 2. Remove specific secrets from history
git filter-branch --tree-filter \
  'sed -i "s/AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng/REDACTED/g" backend/.env' \
  -- --all

# 3. Force push to remote
git push --force --all
git push --force --tags
```

### Option C: Using git-secrets (Prevention)

```bash
# 1. Install git-secrets
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
make install

# 2. Install hooks in your repo
cd InterviewAssistant
git secrets --install

# 3. Add patterns to detect
git secrets --register-aws
git secrets --add 'AIzaSy[A-Za-z0-9_-]{33}'  # Gemini API key pattern
git secrets --add 'postgresql://.*:.*@'      # PostgreSQL connection string
git secrets --add 'password.*=.*'            # Password patterns

# 4. Scan for existing secrets
git secrets --scan-history

# 5. Scan before each commit (automatic with hooks)
git secrets --scan
```

---

## 📝 Complete Cleanup Workflow

### Step-by-Step Commands

```bash
# 1. Navigate to your repository
cd InterviewAssistant

# 2. Verify current status
git status
git log --oneline | head -5

# 3. Create a backup branch (just in case)
git branch backup-before-cleanup

# 4. Remove .env from git tracking (if it was tracked)
git rm --cached backend/.env
git commit -m "security: remove .env from git tracking"

# 5. Update .env.example with placeholder values
# (Already done, but verify)
cat backend/.env.example | head -10

# 6. Add .env to .gitignore (if not already there)
echo ".env" >> .gitignore
git add .gitignore
git commit -m "security: ensure .env is in .gitignore"

# 7. Remove secrets from history using BFG
git clone --mirror https://github.com/yourusername/InterviewAssistant.git
cd InterviewAssistant.git
echo "AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng" > secrets.txt
echo "945725" >> secrets.txt
bfg --replace-text secrets.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
cd ..
rm -rf InterviewAssistant.git

# 8. Verify no secrets remain
git log -p | grep -i "AIzaSy" || echo "✅ No API keys found"
git log -p | grep "945725" || echo "✅ No passwords found"

# 9. Force push to remote
git push --force origin main

# 10. Verify on GitHub
# Go to: https://github.com/yourusername/InterviewAssistant
# Check that .env is not in the repository
# Check git history for any exposed secrets
```

---

## 🔍 Verification Commands

### Verify Secrets Are Removed

```bash
# 1. Search git history for API key
git log -p -S "AIzaSyDCmlxXW9ElegLzDbLrs7i1knm2V7j9wng"
# Should output: (no results)

# 2. Search for password
git log -p -S "945725"
# Should output: (no results)

# 3. Search for database URL
git log -p -S "postgresql://postgres"
# Should output: (no results)

# 4. Check all commits that modified .env
git log --follow -- backend/.env
# Should show only the removal commit

# 5. Verify .env is not in current commit
git show HEAD:backend/.env 2>/dev/null || echo "✅ .env not in HEAD"

# 6. Verify .env is ignored
git check-ignore -v backend/.env
# Should output: .gitignore:5:.env
```

### Verify Setup for Team Members

```bash
# 1. Check that .env is properly ignored
git status | grep ".env"
# Should output nothing

# 2. Verify .env.example exists
ls -la backend/.env.example
# Should exist

# 3. Verify .env is in .gitignore
grep "\.env" .gitignore
# Should output: .env

# 4. Check git history for secrets
git log --all --oneline | wc -l
# Should show total commits

# 5. Scan for any remaining secrets
git secrets --scan-history
# Should output: (no secrets found)
```

---

## 📋 Commands for Team Members

### After You've Cleaned Up

**For each team member to run:**

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create .env from template
cd backend
cp .env.example .env

# 3. Add your credentials
nano .env
# Fill in:
# GOOGLE_API_KEY=your_new_key
# DATABASE_URL=postgresql://user:password@localhost:5432/db

# 4. Verify .env is ignored
git status | grep ".env"
# Should output nothing

# 5. Verify you can run the app
python main.py
# Should start without errors

# 6. Verify git-secrets is working
git secrets --scan
# Should output: (no secrets found)
```

---

## 🛡️ Prevent Future Incidents

### Setup git-secrets Globally

```bash
# 1. Install git-secrets
brew install git-secrets  # macOS
# or download from: https://github.com/awslabs/git-secrets

# 2. Install hooks globally
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets

# 3. Add patterns to detect
git secrets --register-aws
git secrets --add 'AIzaSy[A-Za-z0-9_-]{33}'
git secrets --add 'postgresql://.*:.*@'
git secrets --add 'password.*=.*'

# 4. For existing repo
cd InterviewAssistant
git secrets --install
git secrets --scan-history
```

### Pre-commit Hook

```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Prevent committing .env files
if git diff --cached --name-only | grep -E "\.env$"; then
    echo "❌ ERROR: Attempting to commit .env file!"
    echo "❌ .env files should NEVER be committed"
    exit 1
fi

# Run git-secrets scan
git secrets --scan
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Secrets detected in staged changes"
    exit 1
fi

echo "✅ Pre-commit checks passed"
exit 0
EOF

# Make it executable
chmod +x .git/hooks/pre-commit
```

---

## 🚨 Emergency Response Checklist

If secrets are exposed:

- [ ] **Immediately rotate credentials**
  ```bash
  # Regenerate API keys
  # Change database passwords
  # Update all services
  ```

- [ ] **Remove from git history**
  ```bash
  # Use BFG or git-filter-branch
  git push --force
  ```

- [ ] **Notify team members**
  ```bash
  # Send urgent notification with new credentials
  # Provide setup instructions
  ```

- [ ] **Monitor for abuse**
  ```bash
  # Check API usage logs
  # Monitor database access logs
  # Set up alerts
  ```

- [ ] **Update documentation**
  ```bash
  # Update SECURITY_GUIDE.md
  # Update README.md
  # Commit changes
  ```

---

## 📞 Useful Git Commands Reference

### View History

```bash
# Show commits that modified .env
git log --follow -- backend/.env

# Show all commits with specific content
git log -p -S "search_term"

# Show commits in date range
git log --since="2024-01-01" --until="2024-01-31"

# Show commits by author
git log --author="name"
```

### Undo Changes

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo specific file
git checkout HEAD -- backend/.env

# Undo staged changes
git reset HEAD backend/.env
```

### Clean Up

```bash
# Remove untracked files
git clean -fd

# Remove untracked files and directories
git clean -fdx

# Prune remote branches
git remote prune origin

# Garbage collection
git gc --aggressive
```

### Force Operations

```bash
# Force push (use with caution!)
git push --force origin main

# Force push all branches
git push --force --all

# Force push tags
git push --force --tags

# Force pull (discard local changes)
git reset --hard origin/main
```

---

## ✅ Final Verification

After completing all steps:

```bash
# 1. Verify no secrets in history
git log -p | grep -i "AIzaSy" && echo "❌ FOUND API KEY" || echo "✅ No API keys"
git log -p | grep "945725" && echo "❌ FOUND PASSWORD" || echo "✅ No passwords"

# 2. Verify .env is ignored
git check-ignore -v backend/.env && echo "✅ .env is ignored" || echo "❌ .env is NOT ignored"

# 3. Verify .env.example exists
[ -f backend/.env.example ] && echo "✅ .env.example exists" || echo "❌ .env.example missing"

# 4. Verify git-secrets is working
git secrets --scan && echo "✅ No secrets detected" || echo "❌ Secrets found"

# 5. Verify team can clone and setup
git clone https://github.com/yourusername/InterviewAssistant.git test-clone
cd test-clone
cp backend/.env.example backend/.env
git status | grep ".env" || echo "✅ .env properly ignored"
cd ..
rm -rf test-clone
```

---

## 📚 Resources

- [GitHub: Removing Sensitive Data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [git-secrets](https://github.com/awslabs/git-secrets)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Last Updated:** January 2024
**Status:** Critical Security Guide
**Version:** 1.0.0
