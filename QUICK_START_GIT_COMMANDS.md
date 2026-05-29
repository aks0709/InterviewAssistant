# 🚀 QUICK START - Git Commands to Execute

> Copy-paste ready commands to secure your repository immediately.

---

## ⚠️ BEFORE YOU START

1. **Backup your repository** (just in case)
   ```bash
   git clone https://github.com/yourusername/InterviewAssistant.git InterviewAssistant-backup
   ```

2. **Rotate your credentials** (CRITICAL!)
   - Regenerate Google Gemini API key
   - Change PostgreSQL password
   - Update local `.env` file

3. **Have BFG installed**
   ```bash
   # macOS
   brew install bfg
   
   # Windows (Chocolatey)
   choco install bfg
   
   # Or download: https://rtyley.github.io/bfg-repo-cleaner/
   ```

---

## 🔄 STEP 1: Prepare Your Repository

### 1.1 Verify Current Status
```bash
cd InterviewAssistant
git status
git log --oneline | head -5
```

### 1.2 Create Backup Branch
```bash
git branch backup-before-cleanup
```

### 1.3 Verify .env is in .gitignore
```bash
grep "\.env" .gitignore
# Should output: .env
```

---

## 🧹 STEP 2: Remove Secrets from Git History

### 2.1 Create Mirror Clone
```bash
git clone --mirror https://github.com/yourusername/InterviewAssistant.git InterviewAssistant.git
cd InterviewAssistant.git
```

### 2.2 Create Secrets File
```bash
cat > secrets.txt << EOF
[REDACTED - OLD API KEY]
[REDACTED - OLD PASSWORD]
[REDACTED - OLD DB URL]
EOF
```

### 2.3 Run BFG to Remove Secrets
```bash
bfg --replace-text secrets.txt
```

### 2.4 Clean Up Git History
```bash
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### 2.5 Push Changes Back
```bash
git push --force
```

### 2.6 Clean Up Local Files
```bash
cd ..
rm -rf InterviewAssistant.git
rm secrets.txt
```

---

## ✅ STEP 3: Verify Cleanup

### 3.1 Verify No Secrets in History
```bash
cd InterviewAssistant
git log -p | grep -i "AIzaSy" || echo "✅ No API keys found"
git log -p | grep "[REDACTED]" || echo "✅ No passwords found"
git log -p | grep "postgresql://postgres" || echo "✅ No DB URLs found"
```

### 3.2 Verify .env is Ignored
```bash
git check-ignore -v backend/.env
# Should output: .gitignore:5:.env
```

### 3.3 Verify .env.example Exists
```bash
ls -la backend/.env.example
# Should exist
```

### 3.4 Verify No .env in Current Commit
```bash
git show HEAD:backend/.env 2>/dev/null || echo "✅ .env not in HEAD"
```

---

## 🔐 STEP 4: Setup Prevention Tools

### 4.1 Install git-secrets
```bash
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
make install
cd ..
```

### 4.2 Install Hooks in Repository
```bash
cd InterviewAssistant
git secrets --install
```

### 4.3 Add Patterns to Detect
```bash
git secrets --register-aws
git secrets --add 'AIzaSy[A-Za-z0-9_-]{33}'
git secrets --add 'postgresql://.*:.*@'
git secrets --add 'password.*=.*'
```

### 4.4 Scan History for Secrets
```bash
git secrets --scan-history
# Should output: (no secrets found)
```

---

## 📝 STEP 5: Commit Security Changes

### 5.1 Add Security Files
```bash
git add .gitignore
git add README.md
git add backend/.env.example
git add docs/SECURITY_GUIDE.md
git add docs/GIT_SECURITY_COMMANDS.md
git add SECURITY_IMPLEMENTATION.md
git add SECURITY_FINAL_REPORT.md
```

### 5.2 Commit Changes
```bash
git commit -m "security: implement comprehensive security measures

- Add .env.example with placeholder values
- Enhance .gitignore with comprehensive secret patterns
- Create SECURITY_GUIDE.md with detailed procedures
- Create GIT_SECURITY_COMMANDS.md with cleanup commands
- Update README.md with security setup section
- Add SECURITY_IMPLEMENTATION.md summary
- Add SECURITY_FINAL_REPORT.md verification

This commit addresses the accidental exposure of API credentials
and implements best practices for secret management."
```

### 5.3 Force Push to Remote
```bash
git push --force origin main
```

---

## 👥 STEP 6: Notify Team Members

### 6.1 Send Security Update
Send this message to your team:

```
🔐 SECURITY UPDATE: Repository Credentials Rotated

The Interview Assistant repository had exposed credentials that have been remediated.

ACTION REQUIRED FOR ALL TEAM MEMBERS:
1. Pull latest changes: git pull origin main
2. Create .env from template: cp backend/.env.example backend/.env
3. Add your credentials to .env (I'll send separately)
4. Verify setup: git status | grep .env (should show nothing)

IMPORTANT:
- NEVER commit .env to git
- NEVER share your API keys
- Always use .env.example as template
- See docs/SECURITY_GUIDE.md for details

Questions? See docs/SECURITY_GUIDE.md or contact security team.
```

### 6.2 Provide New Credentials
Send new API keys and database credentials securely (NOT via email/chat):
- Use password manager
- Use secure file sharing
- Use encrypted communication

---

## 🔍 STEP 7: Final Verification

### 7.1 Verify on GitHub
```bash
# Go to: https://github.com/yourusername/InterviewAssistant
# Check that:
# - .env is NOT in the repository
# - .env.example IS in the repository
# - Security files are present
```

### 7.2 Verify Git History
```bash
# Go to: https://github.com/yourusername/InterviewAssistant/commits/main
# Check that:
# - No .env file in history
# - No exposed secrets in commits
```

### 7.3 Verify Team Setup
```bash
# For each team member:
git clone https://github.com/yourusername/InterviewAssistant.git
cd InterviewAssistant
cp backend/.env.example backend/.env
nano backend/.env  # Add credentials
git status | grep ".env"  # Should show nothing
python backend/main.py  # Should start without errors
```

---

## 🛡️ STEP 8: Setup GitHub Secret Scanning

### 8.1 Enable Secret Scanning
1. Go to repository Settings
2. Navigate to "Code security and analysis"
3. Enable "Secret scanning"
4. Enable "Push protection"

### 8.2 Verify Setup
```bash
# Go to: https://github.com/yourusername/InterviewAssistant/security/secret-scanning
# Should show: Secret scanning enabled
```

---

## 📋 COMPLETE CHECKLIST

### Before Cleanup
- [ ] Backup repository
- [ ] Rotate credentials
- [ ] Install BFG
- [ ] Create backup branch

### During Cleanup
- [ ] Create mirror clone
- [ ] Create secrets file
- [ ] Run BFG
- [ ] Clean git history
- [ ] Push changes

### After Cleanup
- [ ] Verify no secrets in history
- [ ] Verify .env is ignored
- [ ] Verify .env.example exists
- [ ] Install git-secrets
- [ ] Scan history for secrets

### Commit & Push
- [ ] Add security files
- [ ] Commit changes
- [ ] Force push to remote
- [ ] Verify on GitHub

### Team & Monitoring
- [ ] Notify team members
- [ ] Provide new credentials
- [ ] Enable GitHub scanning
- [ ] Monitor for abuse

---

## 🚨 TROUBLESHOOTING

### BFG Not Found
```bash
# Download manually
# https://rtyley.github.io/bfg-repo-cleaner/
# Then run:
java -jar bfg-1.14.0.jar --replace-text secrets.txt InterviewAssistant.git
```

### Force Push Rejected
```bash
# Ensure you have permission
# Check branch protection rules
# Temporarily disable if needed
```

### git-secrets Not Working
```bash
# Reinstall hooks
git secrets --install
git secrets --scan-history
```

### Still Seeing Secrets in History
```bash
# Run BFG again with more aggressive settings
bfg --replace-text secrets.txt --no-blob-protection
```

---

## 📞 SUPPORT

### If Something Goes Wrong
1. Use backup branch: `git checkout backup-before-cleanup`
2. Restore from backup: `git clone InterviewAssistant-backup`
3. Contact security team
4. See: `docs/SECURITY_GUIDE.md`

### For Questions
- See: `docs/SECURITY_GUIDE.md`
- See: `docs/GIT_SECURITY_COMMANDS.md`
- See: `SECURITY_IMPLEMENTATION.md`

---

## ✅ SUCCESS INDICATORS

After completing all steps, you should see:

✅ No `.env` file in repository
✅ `.env.example` with placeholder values
✅ No secrets in git history
✅ `.env` in `.gitignore`
✅ Security documentation present
✅ git-secrets installed and working
✅ GitHub secret scanning enabled
✅ Team members notified
✅ New credentials distributed

---

**Status:** Ready to Execute 🚀

**Estimated Time:** 30-45 minutes

**Risk Level:** Low (with backup branch)

**Last Updated:** January 2024
