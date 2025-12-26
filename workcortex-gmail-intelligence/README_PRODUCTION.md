# WorkCortex Gmail Intelligence System

> **Status:** 🔬 TESTING PHASE - OAuth2 authorized users only  
> A production-grade Gmail intelligence system with live execution logs, ML-based identity resolution, and real-time UI streaming.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Google Cloud Setup](#google-cloud-setup)
- [Running the System](#running-the-system)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Code Quality](#code-quality)
- [Testing Limitations](#testing-limitations)

---

## 📋 Overview

WorkCortex Gmail Intelligence is a local Python system that:

1. **Authenticates** with Gmail via OAuth2 (one-time setup)
2. **Fetches all emails** from a specified sender email address
3. **Extracts recipient email addresses** from To, Cc, and Bcc fields
4. **Deduplicates recipients** using explainable ML clustering (sklearn)
5. **Exports to Excel** at a configurable local path
6. **Streams live execution logs** in real-time via Streamlit UI or terminal

### Perfect For:
- 🎓 **Interview Preparation** - Production-grade code with real APIs
- 📊 **Data Analysis** - Extract and deduplicate email recipients
- 🚀 **Learning** - OAuth2, Gmail API, Streamlit, ML clustering
- 🏢 **Demonstration** - Real Gmail integration, live logging

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Real Gmail API** | Uses actual OAuth2, not mocks |
| **Live Execution Logs** | Events emitted DURING execution, streamed real-time |
| **Explainable ML** | sklearn AgglomerativeClustering for identity deduplication |
| **Dual Interface** | CLI (terminal) or Web UI (Streamlit) |
| **Pagination Support** | Handles Gmail API message pagination automatically |
| **Retry Logic** | Built-in retry mechanism for transient failures |
| **Production Code** | Clean, procedural, interview-ready architecture |
| **Thread-Safe Events** | Concurrent event emission and collection |
| **Service Reuse** | No duplicate OAuth consent (single auth per session) |

---

## 🏗️ Architecture

### High-Level Flow

```
┌──────────────────┐
│   User Input     │
│  (OAuth2 Auth)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│   Gmail API Query    │
│ Fetch from:{sender}  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Extract Recipients   │
│ (To/Cc/Bcc headers)  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│   ML Clustering      │
│ Deduplicate emails   │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Export to Excel      │
│ (Pandas + openpyxl)  │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│   Live Logs Stream   │
│ (Throughout entire   │
│    execution)        │
└──────────────────────┘
```

### System Components

```
Backend:
├── events.py          - Thread-safe event queue for live streaming
├── engine.py          - Sequential task executor with retry logic
├── gmail.py           - Real Gmail API integration (OAuth2)
├── ml.py              - sklearn clustering for identity resolution
├── excel.py           - Pandas/openpyxl export
└── main.py            - CLI entry point (interactive)

Frontend:
└── ui/app.py          - Streamlit web interface (real-time logs)

Configuration:
├── credentials.json   - Google OAuth2 credentials (after setup)
├── token.json         - OAuth2 token (auto-generated)
└── requirements.txt   - Python dependencies
```

---

## 🔧 Prerequisites

### System Requirements
- **Python 3.8+** installed
- **pip** package manager available
- **Internet connection** for OAuth2 flow
- **Local ports available:**
  - Port 8080 (OAuth redirect)
  - Port 8501 (Streamlit UI)

### Google Cloud Setup (Required)
- **Google Cloud Console** project access
- **Gmail API enabled**
- **OAuth2 credentials** configured
- **2+ authorized test user accounts** (for testing)

---

## 💾 Installation

### Step 1: Clone/Download Project

```bash
cd workcortex-gmail-intelligence
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.25.0 | Web UI framework |
| pandas | ≥1.3.0 | Data manipulation |
| openpyxl | ≥3.1.0 | Excel writing |
| scikit-learn | ≥0.24.0 | ML clustering |
| google-auth | ≥2.0.0 | OAuth2 authentication |
| google-auth-oauthlib | ≥0.4.6 | OAuth2 flow |
| google-api-python-client | ≥2.50.0 | Gmail API client |
| numpy | ≥1.21.0 | Numerical computing |
| dnspython | ≥2.0.0 | MX record lookup |

---

## 🔐 Google Cloud Setup

This is a **one-time setup** required for OAuth2 authentication.

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Create Project**
3. Enter project name: `gmail-intelligence-482221`
4. Wait for project creation

### Step 2: Enable Gmail API

1. Go to **APIs & Services** → **Library**
2. Search for **"Gmail API"**
3. Click on it
4. Click **Enable**

### Step 3: Create OAuth2 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. When prompted, choose **Desktop application**
4. Name it: `WorkCortex Gmail Intelligence`
5. Click **Create**
6. Click **Download JSON** (right panel)
7. Save as `backend/credentials.json` in your project

### Step 4: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Click **Create Consent Screen**
3. Choose **Testing** (for authorized users only)
4. Fill in required fields:
   - **App name:** WorkCortex Gmail Intelligence
   - **User support email:** Your Gmail address
   - **Required scopes:** Click **Add Scope** and select:
     - `https://www.googleapis.com/auth/gmail.readonly`
5. Under **Test users**, click **Add user** and add both of your test email addresses
6. Click **Save & Continue**

### Step 5: Register Redirect URIs

1. Go to **APIs & Services** → **Credentials**
2. Click on your OAuth 2.0 Client ID
3. Under **Authorized redirect URIs**, add both:
   - `http://localhost:8080/`
   - `http://127.0.0.1:8080/`
4. Click **Save**

### Step 6: Place Credentials in Project

1. Download the updated `credentials.json` from credentials page
2. Place it at: `backend/credentials.json`
3. **IMPORTANT:** Add to `.gitignore`:
   ```
   backend/credentials.json
   backend/token.json
   ```

✅ **Setup Complete!** You're ready to run the system.

---

## 🚀 Running the System

### Option A: Web UI (Recommended) 🌐

```bash
python -m streamlit run ui/app.py
```

Opens browser to **http://localhost:8501**

#### UI Workflow:

1. **Authenticate Section** (Sidebar)
   - Click **🔐 Authenticate with Google**
   - Browser opens to OAuth consent
   - Approve `gmail.readonly` access
   - Returns to app showing authenticated email

2. **Configuration Section** (Main area)
   - Enter **Sender Email**: `upendrachakravarty1@gmail.com`
   - Enter **Output Excel Path**: `C:/Users/YOU/recipients.xlsx`
   - Toggle **Enable ML Deduplication** (optional)
   - Toggle **Verify MX Records** (optional)

3. **Execution Section**
   - Click **🚀 Start Execution**
   - Watch **Live Event Logs** stream in real-time
   - View **Execution Results** when complete

#### Example UI Log Output:

```
Timestamp            | Order | Step                           | Tool           | Status
2025-12-25 16:18:02 |   1   | Fetching Gmail Emails          | Gmail API      | STARTED
2025-12-25 16:18:07 |   1   | Fetching Gmail Emails          | Gmail API      | SUCCESS
2025-12-25 16:18:07 |   2   | Resolving Duplicate Identities | ML Engine      | STARTED
2025-12-25 16:18:07 |   2   | Resolving Duplicate Identities | ML Engine      | SUCCESS
2025-12-25 16:18:07 |   3   | Saving to Excel                | Pandas/Excel   | STARTED
2025-12-25 16:18:08 |   3   | Saving to Excel                | Pandas/Excel   | SUCCESS

Results:
  ✓ Recipients extracted: 12
  ✓ Identities resolved: 10
  ✓ File saved: C:/Users/YOU/recipients.xlsx
```

---

### Option B: CLI (Terminal) 💻

```bash
python -m backend.main
```

#### CLI Workflow:

```
📧 Gmail Intelligence System
============================================================

📧 Enter sender email (e.g., sender@gmail.com): upendrachakravarty1@gmail.com

💾 Enter output Excel path (default: recipients.xlsx): C:/Users/YOU/recipients.xlsx

🤖 Enable ML identity resolution? (yes/no) [default: yes]: yes

🔍 Verify MX records for email validity? (yes/no) [default: no]: no

============================================================
📋 Configuration Summary:
  Authenticated User: your-email@gmail.com
  Sender: upendrachakravarty1@gmail.com
  Output File: C:/Users/YOU/recipients.xlsx
  ML Enabled: Yes
  MX Verification: No
============================================================

[Live execution begins here...]

✅ Pipeline Execution Complete
  Recipients: 12
  Identities: 10
  Output: C:/Users/YOU/recipients.xlsx
```

---

## 📊 Example Output

### Generated Excel File

When the system completes, an Excel file is created:

**File: recipients.xlsx**

| recipient_email | cluster_id |
|-----------------|-----------|
| alice@company.com | 1 |
| bob@example.org | 2 |
| carol@tech.io | 3 |
| david@startup.io | 4 |
| eve.chen@research.org | 5 |
| frank@innovation.io | 6 |
| grace.lee@enterprise.com | 7 |
| henry.brown@education.org | 8 |
| iris.wong@nonprofit.io | 9 |
| jack.kumar@software.dev | 10 |

### Live Execution Logs

**What you see during execution:**

```
Timestamp          | Order | Step                       | Tool      | Status
2025-12-25 16:18:02|   1   | Fetching Gmail Emails     | Gmail     | STARTED
2025-12-25 16:18:05|   1   | Fetching Gmail Emails     | Gmail     | SUCCESS
2025-12-25 16:18:05|   2   | Resolving Identities      | ML        | STARTED
2025-12-25 16:18:06|   2   | Resolving Identities      | ML        | SUCCESS
2025-12-25 16:18:06|   3   | Saving to Excel           | Pandas    | STARTED
2025-12-25 16:18:07|   3   | Saving to Excel           | Pandas    | SUCCESS
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

```bash
# Custom credentials path
export GMAIL_CREDENTIALS_PATH=/path/to/credentials.json

# Custom token path
export GMAIL_TOKEN_PATH=/path/to/token.json
```

### Programmatic Usage

Use as a Python library in your own code:

```python
from backend.main import run_pipeline

# Execute pipeline
success, context, events = run_pipeline(
    sender="sender@gmail.com",
    output_path="C:/Users/YOU/recipients.xlsx",
    enable_ml=True,
    verify_mx=False
)

# Check results
if success:
    print(f"Recipients extracted: {context['recipient_count']}")
    print(f"Identities resolved: {context['identity_count']}")
    print(f"Excel saved to: {context['excel_path']}")
    
    # Print all events
    for event in events:
        print(f"{event['timestamp']} | {event['step']} | {event['status']}")
```

---

## 🔍 How It Works

### Component 1: Gmail API Integration

**File:** `backend/gmail.py`

```python
def fetch_emails(context):
    """
    1. Authenticate with OAuth2 (uses token.json if available)
    2. Query Gmail for all emails from sender
    3. Extract recipient email addresses from To/Cc/Bcc
    4. Return deduplicated list
    """
```

**Key Features:**
- ✅ OAuth2 with automatic token refresh
- ✅ Gmail query: `from:{sender}` (fetches all emails from that sender)
- ✅ Pagination support (handles 100+ messages)
- ✅ Header parsing (To, Cc, Bcc extraction)
- ✅ Debug logging for troubleshooting

**Example Output:**
```
Found 27 emails from upendrachakravarty1@gmail.com
Extracted 14 recipients from To/Cc/Bcc headers
Unique recipients: 12
```

---

### Component 2: ML Identity Resolution

**File:** `backend/ml.py`

```python
def resolve_identities(emails):
    """
    1. Normalize email addresses (remove dots/underscores)
    2. Create feature vectors for clustering
    3. Use sklearn AgglomerativeClustering to group similar emails
    4. Keep one email per cluster (identity)
    5. Return deduplicated list
    """
```

**Why This is Valid ML:**
- ✅ Feature extraction (normalization)
- ✅ Unsupervised learning (clustering without labels)
- ✅ Explainable (can show which emails grouped together)
- ✅ No deep learning black box
- ✅ Reproducible and deterministic

**Example Clustering:**
```
Raw emails:
  - john.doe@company.com
  - johndoe@company.com
  - j.doe@company.com
  
After normalization:
  - johndoe
  - johndoe
  - jdoe
  
Clustering result:
  Cluster 1: [john.doe@company.com, johndoe@company.com]  → Keep: john.doe@company.com
  Cluster 2: [j.doe@company.com]  → Keep: j.doe@company.com
```

---

### Component 3: Excel Export

**File:** `backend/excel.py`

```python
def save_excel(context):
    """
    1. Get deduplicated email list from context
    2. Create Pandas DataFrame
    3. Write to Excel using openpyxl
    4. Ensure output directory exists
    """
```

**Output Format:**
- Single sheet: "Recipients"
- Column: `recipient_email`
- Rows: Sorted, unique email addresses
- Format: Simple, analysis-ready

---

### Component 4: Live Event Logging

**File:** `backend/events.py`

```python
def emit(order, step, tool, status):
    """
    Emit event to thread-safe queue:
    - order: Step execution order (1, 2, 3, ...)
    - step: Human-readable name (e.g., "Fetching Gmail Emails")
    - tool: Technology used (e.g., "Gmail API")
    - status: STARTED, SUCCESS, FAILED, or RETRIED
    
    Events flow from backend → UI/CLI in real-time
    """
```

**Event Stream:**
```
[STARTED]  → Backend begins step
[SUCCESS]  → Step completed
[FAILED]   → Step failed
[RETRIED]  → Retry attempted
```

**Why This Matters:**
- ✅ See execution progress in real-time
- ✅ Identify exact failure point
- ✅ No "hanging" or invisible progress
- ✅ Demo-friendly and trustworthy

---

### Component 5: Execution Engine

**File:** `backend/engine.py`

```python
class ExecutionEngine:
    def add_step(self, order, name, tool, func, retries=0):
        """Register a step with optional retry logic"""
        
    def run(self, context):
        """
        1. Execute steps in order
        2. Emit STARTED event
        3. If fails: retry up to N times, emit RETRIED
        4. Emit SUCCESS or FAILED
        5. Collect all events
        """
```

**Features:**
- ✅ Sequential execution (not parallel)
- ✅ Configurable retries per step
- ✅ Context passes through steps
- ✅ All events collected and returned
- ✅ Graceful failure handling

---

## 🐛 Troubleshooting

### Problem: "Access blocked: This app's request is invalid"

**Cause:** OAuth consent screen not properly configured

**Solution:**
1. Go to Google Cloud Console → **APIs & Services** → **OAuth consent screen**
2. Click **EDIT APP**
3. Verify all required fields are filled:
   - App name ✓
   - User support email ✓
   - Scopes ✓
   - Test users ✓
4. Click **Save & Continue**
5. Re-download `credentials.json`
6. Replace `backend/credentials.json`

---

### Problem: "redirect_uri_mismatch"

**Cause:** Redirect URIs not registered

**Solution:**
1. Go to **Credentials** → Your OAuth 2.0 Client ID
2. Under **Authorized redirect URIs**, verify you have:
   - `http://localhost:8080/`
   - `http://127.0.0.1:8080/`
3. Click **Save**
4. Re-download credentials.json if changed

---

### Problem: Excel file created but empty (0 recipients)

**Cause:** No emails found from specified sender

**Diagnosis:**
1. Check terminal output for `[DEBUG]` lines:
   ```
   [DEBUG] Searching Gmail with query: from:upendrachakravarty1@gmail.com
   [DEBUG] Found X messages
   [DEBUG] Extracted Y recipients
   ```

2. If found 0 messages:
   - Verify sender email is correct (case-insensitive)
   - Verify you have actual emails FROM that sender in your mailbox
   - The sender email must have sent at least one email to you

3. If found messages but 0 recipients:
   - Some emails may be missing To/Cc/Bcc headers
   - Check if emails are forwarded (may have different headers)

---

### Problem: "Port 8080 already in use"

**Cause:** Another application is using port 8080

**Solution:**
```bash
# Option 1: Kill process using port 8080
netstat -ano | findstr :8080          # Find process ID
taskkill /PID <ProcessID> /F          # Kill it

# Option 2: Use different port
# Currently hardcoded to 8080 in backend/gmail.py
# To change: Edit line 50 in backend/gmail.py:
#   flow.run_local_server(port=8081)
```

---

### Problem: Streamlit shows "Missing ScriptRunContext"

**Status:** Fixed in current version (synchronous execution)

If you see this warning, it's harmless and can be ignored.

---

## 📚 Code Quality

This project demonstrates professional Python engineering:

### Architecture Principles
- ✅ **Separation of Concerns** - Each module has single responsibility
- ✅ **Event-Driven** - Live logging throughout execution
- ✅ **Testable** - Functions accept context, return results
- ✅ **Configurable** - CLI options, environment variables
- ✅ **Reproducible** - No randomness, deterministic output
- ✅ **Safe** - No hard-coded credentials, OAuth only
- ✅ **Documented** - Every function has clear docstring

### Code Statistics

| File | Lines | Purpose |
|------|-------|---------|
| `backend/gmail.py` | 174 | Gmail API integration |
| `backend/ml.py` | 85 | ML clustering |
| `backend/excel.py` | 40 | Excel export |
| `backend/engine.py` | 52 | Task execution |
| `backend/events.py` | 64 | Event streaming |
| `backend/main.py` | 130 | CLI entry point |
| `ui/app.py` | 257 | Streamlit UI |
| **Total** | **802** | Production-grade system |

### Interview-Ready Aspects

Perfect for demonstrating:
1. **Real API Integration** - Not mocks or demos
2. **OAuth2 Flow** - Secure, industry-standard auth
3. **Python Architecture** - Clean, modular design
4. **ML/Data Science** - sklearn, pandas, numpy
5. **Web UI** - Streamlit real-time streaming
6. **CLI Design** - Interactive, user-friendly input
7. **Error Handling** - Graceful degradation
8. **Live Logging** - Thread-safe event queues
9. **Git-Ready** - Proper structure, `.gitignore`, docs
10. **Explainability** - Every line explained

---

## ⚠️ Testing Limitations

**Current Status: 🔬 TESTING PHASE**

This system is fully functional but has limitations for production use:

### What Works
✅ Real Gmail API OAuth2 authentication  
✅ Email fetching and recipient extraction  
✅ ML-based identity deduplication  
✅ Excel export  
✅ Live execution logging  
✅ CLI and web UI interfaces  

### What's Limited
⏳ **OAuth2 Testing Mode**
- Requires Google Cloud Console "Testing" status
- Limited to pre-authorized test users only
- Cannot handle arbitrary Google accounts

⏳ **Gmail API Quota**
- 10,000 grant creation limit per day (testing limit)
- 10,000 refresh token creation limit (testing limit)

⏳ **Message Limits**
- Currently limited to ~100 messages per query
- Can be extended with pagination refactoring

### Path to Production

To move to production:

1. **Set OAuth Consent to "Production"**
   - Requires app verification (Google review process)
   - Allows any Google account access
   - ~1-2 weeks for approval

2. **Increase API Quotas**
   - File quota increase request in Google Cloud Console
   - Usually approved within 24 hours

3. **Add Service Account Support**
   - Use service account (no user consent needed)
   - Requires domain-wide delegation
   - Better for backend automation

4. **Implement Rate Limiting**
   - Add exponential backoff
   - Cache results for performance

---

## 📞 Support & FAQ

### Can I use this with multiple Gmail accounts?

Yes, but each run requires separate OAuth:
```bash
# First run: Use Account A
python -m streamlit run ui/app.py
# Browser: Sign in with Account A
# Complete pipeline

# Second run: Use Account B
# token.json is overwritten
python -m streamlit run ui/app.py
# Browser: Sign in with Account B
```

---

### Can I automate this without browser popup?

Not yet. Current system requires OAuth consent flow.

**Alternative for automation:**
1. Use service account (no user consent)
2. Requires Google Workspace domain
3. Requires domain-wide delegation

---

### How do I save credentials securely?

**Current approach (Testing):**
- `credentials.json` - Published OAuth client (safe to share)
- `token.json` - OAuth access token (DO NOT share)

**Production approach:**
- Store in environment variables
- Use secrets manager (GitHub Secrets, Azure Key Vault)
- Implement credential rotation

---

### Can I filter emails by date?

Yes, modify the Gmail query in `backend/gmail.py` line 113:

```python
# Current:
query = f"from:{sender}"

# With date range:
query = f"from:{sender} after:2025-01-01 before:2025-12-31"

# With subject:
query = f"from:{sender} subject:invoice"
```

See [Gmail Search Operators](https://support.google.com/mail/answer/7190) for more options.

---

### Can I extract other email fields (subject, date, body)?

Yes, extend `backend/gmail.py` `fetch_emails()` function:

```python
# Currently extracts:
headers = message['payload']['headers']
to = next((h['value'] for h in headers if h['name'] == 'To'), '')

# You can also get:
subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
from_addr = next((h['value'] for h in headers if h['name'] == 'From'), '')
```

---

## 🎓 Learning Resources

### OAuth2 in Python
- [Google Auth Python Docs](https://googleapis.dev/python/google-auth/latest/)
- [OAuth2 Explained](https://oauth.net/2/)

### Gmail API
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Gmail Search Operators](https://support.google.com/mail/answer/7190)

### ML Clustering
- [sklearn AgglomerativeClustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html)
- [Clustering Algorithms](https://en.wikipedia.org/wiki/Cluster_analysis)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Real-time Streaming](https://docs.streamlit.io/library/api-reference/write-stream/write_stream)

---

## 📝 Project Details

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.8+ |
| **Framework** | Streamlit 1.25.0+ |
| **APIs** | Gmail API v1 (OAuth2) |
| **Libraries** | pandas, scikit-learn, openpyxl |
| **Architecture** | Event-driven, modular |
| **Code Quality** | Interview-ready |
| **Status** | Testing phase (authorized users only) |
| **License** | Demonstration/Educational |

---

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Set up Google Cloud OAuth
3. ✅ Download credentials.json
4. ✅ Run Streamlit UI or CLI
5. ✅ Send test emails and execute pipeline
6. ✅ Verify Excel output

---

**Built with ❤️ for demonstration excellence**

Last Updated: December 25, 2025  
Version: 1.0 (Testing Phase)
