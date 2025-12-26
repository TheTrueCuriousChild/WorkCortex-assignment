# WorkCortex Gmail Intelligence System

> **Status:** 🔬 TESTING PHASE - OAuth2 authorized users only  
> A production-grade Gmail intelligence system built with real APIs, live execution logs, and explainable ML clustering.

## ⚡ Quick Links

📖 **[Full Documentation](README_PRODUCTION.md)** – Complete setup guide, architecture, troubleshooting  
🚀 **[Quick Start](#quick-start)** – Get running in 5 minutes  
🔐 **[Google Cloud Setup](#google-cloud-setup)** – OAuth2 configuration  

---

## 📌 What Is This?

A local Python system that:

1. 🔐 Authenticates with Gmail via **real OAuth2** (not mocks)
2. 📧 Fetches all emails from a specified **sender email address**
3. 📋 Extracts **recipient email addresses** from To, Cc, Bcc headers
4. 🤖 **Deduplicates recipients** using explainable ML (sklearn clustering)
5. 📊 **Exports to Excel** at your specified path
6. 📡 **Streams live execution logs** in real-time (Streamlit UI or CLI)

### Why This Project?

Perfect for:
- 🎓 **Interview prep** - Production code with real Gmail API
- 📊 **Data extraction** - Recipient analysis from Gmail
- 🚀 **Learning** - OAuth2, Streamlit, ML clustering
- 💼 **Demonstration** - Real integration, not a demo

---

## 🚀 Quick Start

### 1. Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

### 2. Set Up Google OAuth (10 minutes)

👉 **[See full Google Cloud setup guide](README_PRODUCTION.md#google-cloud-setup)** for detailed steps

Quick summary:
1. Create Google Cloud project
2. Enable Gmail API
3. Create OAuth2 credentials → Download `credentials.json`
4. Configure OAuth consent screen
5. Add test users
6. Place `credentials.json` in `backend/` folder

### 3. Run the System (1 minute)

**Option A: Web UI (Recommended)**
```bash
python -m streamlit run ui/app.py
```
Opens: http://localhost:8501

**Option B: CLI (Terminal)**
```bash
python -m backend.main
```

---

## 🎯 How To Use

### Web UI Flow

```
1. Click 🔐 Authenticate with Google
   → Browser opens OAuth consent
   → You approve access
   
2. Enter sender email: upendrachakravarty1@gmail.com
   
3. Enter output Excel path: C:/Users/YOU/recipients.xlsx
   
4. Click 🚀 Start Execution
   
5. Watch live logs stream
   
6. View results → File saved ✓
```

### CLI Flow

```bash
$ python -m backend.main

📧 Enter sender email: upendrachakravarty1@gmail.com
💾 Enter output Excel path: C:/Users/YOU/recipients.xlsx
🤖 Enable ML? (yes/no): yes

[Live execution...]

✅ Complete
   Recipients: 12
   File: C:/Users/YOU/recipients.xlsx
```

---

## 📊 Example Output

**Generated Excel File:**

| recipient_email | 
|-----------------|
| alice@company.com |
| bob@example.org |
| carol@tech.io |
| david@startup.io |

**Live Execution Logs:**

```
Timestamp          | Order | Step                  | Tool    | Status
2025-12-25 16:18:02|   1   | Fetching Gmail       | Gmail   | STARTED
2025-12-25 16:18:05|   1   | Fetching Gmail       | Gmail   | SUCCESS
2025-12-25 16:18:05|   2   | ML Deduplication     | ML      | STARTED
2025-12-25 16:18:06|   2   | ML Deduplication     | ML      | SUCCESS
2025-12-25 16:18:06|   3   | Save to Excel        | Pandas  | STARTED
2025-12-25 16:18:07|   3   | Save to Excel        | Pandas  | SUCCESS
```

---

## 🏗️ System Architecture

```
User Input (OAuth2 Auth)
         ↓
Gmail API Query (from:{sender})
         ↓
Extract Recipients (To/Cc/Bcc)
         ↓
ML Clustering (deduplicate)
         ↓
Export to Excel
         ↓
[Live Event Logs Throughout]
```

### Components

| File | Purpose |
|------|---------|
| `backend/gmail.py` | Real Gmail API integration (OAuth2) |
| `backend/ml.py` | sklearn clustering for identity resolution |
| `backend/excel.py` | Pandas/openpyxl export |
| `backend/engine.py` | Sequential task executor with retry logic |
| `backend/events.py` | Thread-safe event queue (live logging) |
| `backend/main.py` | CLI entry point |
| `ui/app.py` | Streamlit web interface |

---

## ⚙️ Configuration

### Environment Variables (Optional)

```bash
export GMAIL_CREDENTIALS_PATH=/path/to/credentials.json
export GMAIL_TOKEN_PATH=/path/to/token.json
```

### Use as Python Library

```python
from backend.main import run_pipeline

success, context, events = run_pipeline(
    sender="sender@gmail.com",
    output_path="C:/Users/YOU/recipients.xlsx",
    enable_ml=True
)

if success:
    print(f"Recipients: {context['recipient_count']}")
    print(f"Identities: {context['identity_count']}")
```

---

## 🔧 Troubleshooting

### "Access blocked: This app's request is invalid"
→ OAuth consent screen not configured. [See full guide](README_PRODUCTION.md#troubleshooting)

### "redirect_uri_mismatch"
→ Add `http://localhost:8080/` to authorized redirect URIs. [See setup guide](README_PRODUCTION.md#google-cloud-setup)

### Excel file empty
→ Verify sender email has sent emails to you. Check terminal `[DEBUG]` output.

### Port 8080 already in use
→ Change port in `backend/gmail.py` line 50 or kill other process.

**👉 [More troubleshooting](README_PRODUCTION.md#troubleshooting)**

---

## 📚 Dependencies

```
streamlit>=1.25.0
pandas>=1.3.0
openpyxl>=3.1.0
scikit-learn>=0.24.0
google-auth>=2.0.0
google-auth-oauthlib>=0.4.6
google-api-python-client>=2.50.0
numpy>=1.21.0
dnspython>=2.0.0
```

---

## 📖 Full Documentation

👉 **[See README_PRODUCTION.md](README_PRODUCTION.md)** for:
- ✅ Detailed Google Cloud setup
- ✅ Complete architecture explanation
- ✅ How each component works
- ✅ Advanced troubleshooting
- ✅ Production deployment path
- ✅ Interview preparation guide
- ✅ Learning resources
- ✅ Code quality explanations

---

## ⚠️ Testing Phase Notice

**Status: 🔬 TESTING PHASE**

This system is fully functional but currently limited to:
- ✅ OAuth2 authorized test users only
- ✅ Testing mode (requires Google verification for production)
- ✅ 10,000 grant/refresh token daily quota

**Path to production:** See [README_PRODUCTION.md](README_PRODUCTION.md#path-to-production)

---

## 📝 Project Info

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.8+ |
| **Framework** | Streamlit 1.25.0+ |
| **APIs** | Gmail API v1 (OAuth2) |
| **Code Size** | ~800 lines (production-quality) |
| **Interfaces** | Web UI + CLI |
| **Status** | Testing phase |

---

## 🎓 Interview-Ready Features

- ✅ Real OAuth2 integration (not mocks)
- ✅ Production code architecture
- ✅ Event-driven live logging
- ✅ sklearn ML clustering
- ✅ Pandas data processing
- ✅ Streamlit web interface
- ✅ CLI design
- ✅ Error handling
- ✅ Explainable code
- ✅ Git-ready structure

---

**Built with ❤️ for demonstration excellence**

Version: 1.0 (Testing Phase)  
Last Updated: December 25, 2025
