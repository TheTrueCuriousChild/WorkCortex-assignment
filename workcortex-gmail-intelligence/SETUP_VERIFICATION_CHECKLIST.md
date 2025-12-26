# 🚀 WorkCortex Gmail Intelligence - Setup & Verification Checklist

> **Last Updated:** December 25, 2025  
> **Status:** Production-Ready (Testing Phase)

---

## ✅ Pre-Setup Verification

### System Requirements
- [ ] Python 3.8+ installed
- [ ] pip package manager available
- [ ] Internet connection (for OAuth2)
- [ ] Ports 8080 and 8501 available (not in use)
- [ ] Google Account (2+ accounts for testing)

### Google Account Requirements
- [ ] Google Account #1 (authenticated user)
- [ ] Google Account #2 (optional, for testing)
- [ ] Google Cloud Console access
- [ ] Ability to enable APIs
- [ ] Ability to create OAuth credentials

Check: `python --version` should show 3.8+

---

## ✅ Installation Checklist

### Step 1: Install Dependencies
```bash
cd workcortex-gmail-intelligence
pip install -r requirements.txt
```

Verify:
- [ ] Streamlit installed: `pip show streamlit`
- [ ] Pandas installed: `pip show pandas`
- [ ] Openpyxl installed: `pip show openpyxl`
- [ ] scikit-learn installed: `pip show scikit-learn`
- [ ] Google Auth installed: `pip show google-auth`
- [ ] All 9 packages from requirements.txt installed

### Step 2: Verify Project Structure
```bash
ls -la backend/
ls -la ui/
```

Check these files exist:
- [ ] `backend/gmail.py` (174 lines)
- [ ] `backend/ml.py` (85 lines)
- [ ] `backend/excel.py` (40 lines)
- [ ] `backend/engine.py` (52 lines)
- [ ] `backend/events.py` (64 lines)
- [ ] `backend/main.py` (130 lines)
- [ ] `ui/app.py` (257 lines)
- [ ] `requirements.txt` (9 packages)

### Step 3: Verify Documentation
Check these files exist:
- [ ] `README.md` (~1,200 words)
- [ ] `README_PRODUCTION.md` (~4,500 words)
- [ ] `DOCUMENTATION_GUIDE.md` (this file)
- [ ] `requirements.txt` (with all dependencies)

---

## 🔐 Google Cloud Setup Checklist

### Phase 1: Create Project

**Google Cloud Console → Create Project**

- [ ] Project name: `gmail-intelligence-482221`
- [ ] Wait for project creation
- [ ] Project ID: Note it down

**Action Items:**
- [ ] Switch to new project in Console
- [ ] Enable billing (may be required)

---

### Phase 2: Enable Gmail API

**Google Cloud Console → APIs & Services → Library**

- [ ] Search: "Gmail API"
- [ ] Click on Gmail API
- [ ] Click **Enable**

**Verify:** 
- [ ] Gmail API shows as "Enabled"

---

### Phase 3: Create OAuth2 Credentials

**Google Cloud Console → APIs & Services → Credentials**

1. Click **Create Credentials**
   - [ ] Choose: OAuth 2.0 Client ID
   - [ ] If prompted, first configure consent screen ↓

2. Create OAuth Consent Screen
   - [ ] Choose: **External**
   - [ ] Click **Create**
   - App name: `WorkCortex Gmail Intelligence`
   - User support email: [Your email]
   - Click **Save & Continue**

3. Add Scopes
   - [ ] Click **Add Scope**
   - [ ] Search: "gmail.readonly"
   - [ ] Select: `https://www.googleapis.com/auth/gmail.readonly`
   - [ ] Click **Update**
   - [ ] Click **Save & Continue**

4. Add Test Users
   - [ ] Click **Add user** (under Test users)
   - [ ] Add email: [Your Gmail account 1]
   - [ ] Add email: [Your Gmail account 2] (optional)
   - [ ] Click **Save & Continue**

5. Review & Publish
   - [ ] Review app configuration
   - [ ] Click **Save & Continue**
   - [ ] Back to OAuth consent screen
   - [ ] Verify **Testing** status shown

---

### Phase 4: Create OAuth2 Client ID

**Google Cloud Console → APIs & Services → Credentials**

1. Click **+ Create Credentials** (top of page)
   - [ ] Choose: **OAuth 2.0 Client ID**

2. Application Type
   - [ ] Select: **Desktop application**
   - [ ] Name: `WorkCortex Gmail Intelligence`
   - [ ] Click **Create**

3. Download Credentials
   - [ ] Click **Download JSON** (right panel)
   - [ ] Save file as: `credentials.json`
   - [ ] Locate: Now `credentials.json` is in Downloads

**Action Items:**
- [ ] Move/copy `credentials.json` to `backend/` folder
- [ ] Verify: `backend/credentials.json` exists

---

### Phase 5: Register Redirect URIs

**Google Cloud Console → APIs & Services → Credentials**

1. Click on your **OAuth 2.0 Client ID**

2. Under **Authorized redirect URIs**:
   - [ ] Add: `http://localhost:8080/`
   - [ ] Add: `http://127.0.0.1:8080/`
   - [ ] Click **Save**

**Verify:**
- [ ] Both URIs show in the list
- [ ] Settings saved

---

### Phase 6: Verify Setup

**Google Cloud Console → APIs & Services**

- [ ] Gmail API: **Enabled** ✓
- [ ] OAuth 2.0 Client ID: **Created** ✓
- [ ] Consent Screen: **Testing** ✓
- [ ] Test Users: **2+ added** ✓
- [ ] Redirect URIs: **Both added** ✓

**Local Files:**
- [ ] `backend/credentials.json`: **Exists** ✓
- [ ] Contains: `client_id`, `client_secret`
- [ ] `.gitignore`: Includes `credentials.json` ✓

---

## 🚀 Running the System Checklist

### Pre-Run Checks

**Port Availability:**
```powershell
netstat -ano | findstr :8080    # Should show nothing or your app
netstat -ano | findstr :8501    # Should show nothing
```

- [ ] Port 8080 available (OAuth redirect)
- [ ] Port 8501 available (Streamlit)
- [ ] Internet connection active

**Python Environment:**
```bash
python --version                 # Should be 3.8+
pip list | grep streamlit       # Should show streamlit
```

- [ ] Python 3.8+ available
- [ ] All packages installed
- [ ] No virtual environment issues

---

### Option A: Run Web UI

**Step 1: Start Streamlit**
```bash
python -m streamlit run ui/app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

- [ ] No errors in terminal
- [ ] Port 8501 showing
- [ ] Browser can access http://localhost:8501

**Step 2: Authenticate**
- [ ] Click **🔐 Authenticate with Google**
- [ ] Browser opens Google login
- [ ] Sign in with authorized test account
- [ ] Approve `gmail.readonly` scope
- [ ] App shows: "Authenticated as: [your-email@gmail.com]"

**Step 3: Configure**
- [ ] Enter **Sender Email**: `upendrachakravarty1@gmail.com`
- [ ] Enter **Output Path**: `C:/Users/YOU/recipients.xlsx`
- [ ] Toggle **Enable ML**: Yes
- [ ] Toggle **Verify MX**: No (optional)

**Step 4: Execute**
- [ ] Click **🚀 Start Execution**
- [ ] See **Live Event Logs** appear
- [ ] See status change from STARTED → SUCCESS
- [ ] See **Execution Results** section populated
- [ ] See **Recipients count** > 0 (if emails found)

**Step 5: Verify Output**
- [ ] Excel file created at specified path
- [ ] Open file and verify:
  - [ ] Column header: `recipient_email`
  - [ ] Data rows: Email addresses
  - [ ] No errors in cells

**Step 6: Check Logs** (optional)
- [ ] Terminal shows `[DEBUG]` messages:
  - [ ] Message count from Gmail
  - [ ] Recipient extraction count
  - [ ] Final recipient list
  - [ ] MX verification results

---

### Option B: Run CLI

**Step 1: Start CLI**
```bash
python -m backend.main
```

**Expected Prompt:**
```
📧 Gmail Intelligence System
----
📧 Enter sender email: 
```

- [ ] No errors
- [ ] CLI shows prompts

**Step 2: Enter Configuration**
- [ ] Sender email: `upendrachakravarty1@gmail.com`
- [ ] Output path: `C:/Users/YOU/recipients.xlsx`
- [ ] ML enabled: `yes`
- [ ] MX verify: `no`

**Step 3: First Run Authentication**
- [ ] Browser opens (first time only)
- [ ] OAuth consent screen appears
- [ ] You approve access
- [ ] CLI shows: "Authenticated as: [your-email@gmail.com]"
- [ ] `backend/token.json` created

**Step 4: Pipeline Execution**
- [ ] Live logs appear in terminal
- [ ] Each step shows: STARTED → SUCCESS
- [ ] Final results show:
  - [ ] Recipients extracted: X
  - [ ] Identities resolved: Y
  - [ ] File saved: [path]

**Step 5: Verify Output**
- [ ] Excel file exists at specified path
- [ ] Open and verify data

---

## 📊 Data Verification Checklist

### Email Setup
Before testing, ensure:
- [ ] Have sent at least 1 email from Account #2 to Account #1
- [ ] Email contains at least 1 recipient in To/Cc/Bcc
- [ ] Email is in Account #1's mailbox

**Test Scenario:**
1. Use Account A: `your-email@gmail.com`
2. Send email FROM Account B: `sender@gmail.com`
3. Run system with:
   - Authenticated as: Account A
   - Sender email: `sender@gmail.com`
4. System finds emails from Account B in Account A's mailbox

### Excel File Verification
```
Expected columns:
- recipient_email

Expected rows:
- One email per row
- Deduplicated (no duplicates)
- Sorted alphabetically

Example:
recipient_email
alice@company.com
bob@example.org
carol@tech.io
```

- [ ] File created without errors
- [ ] File opens in Excel
- [ ] Header row: `recipient_email`
- [ ] Data rows: Email addresses
- [ ] No duplicate emails (ML deduplication worked)
- [ ] Emails are sorted

### Log Verification
```
Expected events:
1. Fetching Gmail Emails | STARTED
2. Fetching Gmail Emails | SUCCESS
3. Resolving Duplicate Identities | STARTED
4. Resolving Duplicate Identities | SUCCESS
5. Saving to Excel | STARTED
6. Saving to Excel | SUCCESS
```

- [ ] All 6 events appear
- [ ] All steps show SUCCESS
- [ ] No FAILED events
- [ ] No RETRIED events
- [ ] Timestamps progress forward

---

## 🐛 Troubleshooting Checklist

### Issue: "Access blocked: This app's request is invalid"

**Root Cause:** OAuth consent screen not configured properly

**Fix Steps:**
- [ ] Go to Google Cloud Console
- [ ] Go to OAuth consent screen
- [ ] Click **EDIT APP**
- [ ] Verify all required fields filled:
  - [ ] App name ✓
  - [ ] User support email ✓
  - [ ] Scopes added ✓
  - [ ] Test users added ✓
- [ ] Click **Save & Continue** on each step
- [ ] Download credentials.json again
- [ ] Replace `backend/credentials.json`
- [ ] Delete `backend/token.json` (force fresh auth)
- [ ] Re-run system

---

### Issue: "redirect_uri_mismatch"

**Root Cause:** Redirect URI not registered

**Fix Steps:**
- [ ] Go to Credentials → OAuth 2.0 Client ID
- [ ] Under **Authorized redirect URIs**:
  - [ ] Add: `http://localhost:8080/`
  - [ ] Add: `http://127.0.0.1:8080/`
- [ ] Click **Save**
- [ ] Download credentials.json again
- [ ] Replace `backend/credentials.json`
- [ ] Delete `backend/token.json`
- [ ] Re-run system

---

### Issue: Excel File Empty (0 Recipients)

**Root Causes:** 
1. No emails found from sender
2. Emails have no To/Cc/Bcc headers
3. Query is too restrictive

**Debug Steps:**
- [ ] Check terminal for `[DEBUG]` output:
  ```
  [DEBUG] Searching Gmail with query: from:sender@gmail.com
  [DEBUG] Found X messages
  [DEBUG] Extracted Y recipients
  ```
- [ ] Verify sender email is correct (case-insensitive)
- [ ] Verify you have actual emails FROM that sender
- [ ] Try a different sender email that sent you emails
- [ ] Check terminal [DEBUG] lines for error messages

**Manual Test:**
```bash
# Go to Gmail, try this search:
from:sender@gmail.com
# Should show emails from that sender
```

---

### Issue: Port 8080 Already in Use

**Root Cause:** Another app using port 8080

**Fix Options:**

**Option 1: Kill Process**
```powershell
# Find process using port 8080
netstat -ano | findstr :8080

# Kill it (replace XXXX with PID)
taskkill /PID XXXX /F
```

**Option 2: Change Port**
Edit `backend/gmail.py` line ~50:
```python
# Change from:
flow.run_local_server(port=8080)
# To:
flow.run_local_server(port=8081)
```

- [ ] Port changed (if using Option 2)
- [ ] `backend/gmail.py` saved
- [ ] Re-run system

---

### Issue: "No module named 'streamlit'"

**Root Cause:** Dependencies not installed

**Fix:**
```bash
pip install -r requirements.txt
```

- [ ] Command completed without errors
- [ ] Run: `pip list | grep streamlit`
- [ ] Shows streamlit version

---

## 🎓 Interview Prep Checklist

If using for interview demonstration:

### Code Review
- [ ] Read through `backend/gmail.py` completely
- [ ] Understand OAuth2 flow
- [ ] Know how Gmail API query works
- [ ] Understand how recipients are extracted

### ML Understanding
- [ ] Read through `backend/ml.py`
- [ ] Understand normalization approach
- [ ] Know what AgglomerativeClustering does
- [ ] Be able to explain why this is ML
- [ ] Know advantages/limitations

### Architecture Understanding
- [ ] Draw architecture diagram from memory
- [ ] Explain event-driven design
- [ ] Explain execution engine flow
- [ ] Explain why design is testable

### Demo Confidence
- [ ] Run system multiple times
- [ ] Know each step from memory
- [ ] Can explain what each button does
- [ ] Understand what happens behind scenes
- [ ] Know what could fail and how to debug

### Business Understanding
- [ ] Know the problem this solves
- [ ] Know use cases for recipient extraction
- [ ] Know why deduplication matters
- [ ] Know production limitations (Testing phase)
- [ ] Know path to production

---

## 📋 Final Checklist

### Before Sharing with Others
- [ ] README.md is clear and complete
- [ ] README_PRODUCTION.md is comprehensive
- [ ] All links in docs work
- [ ] Code examples are accurate
- [ ] Google Cloud setup guide is correct
- [ ] System works end-to-end on your machine
- [ ] Excel file generates correctly
- [ ] Live logs display properly
- [ ] No hard-coded passwords/tokens
- [ ] `.gitignore` includes credentials

### Before GitHub Submission
- [ ] All files committed (except credentials)
- [ ] README.md is main documentation
- [ ] GitHub recognizes it as main README
- [ ] Code is clean and commented
- [ ] No uncommitted changes
- [ ] Git history is clean
- [ ] Project is public/visible
- [ ] Description is clear on GitHub

### Before Job Interview
- [ ] System runs smoothly without delays
- [ ] Can explain every line
- [ ] Know limitations and constraints
- [ ] Have production plan documented
- [ ] Can discuss design decisions
- [ ] Ready to answer advanced questions
- [ ] Can show code examples
- [ ] Understand all technologies used

---

## ✅ Sign Off

**System Setup Status:** _______________

**Date Verified:** _______________

**Verified By:** _______________

**Ready for Submission:** ☐ Yes ☐ No

**Next Steps:** _________________________________________________

---

**Last Updated:** December 25, 2025  
**Version:** 1.0 (Testing Phase)  
**Status:** ✅ Ready for Production Use (authorized users only)
