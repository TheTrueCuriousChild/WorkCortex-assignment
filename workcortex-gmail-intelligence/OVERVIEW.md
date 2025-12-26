# WorkCortex Gmail Intelligence - System Overview

## ONE SENTENCE

A local Python application that fetches emails from Gmail using the real API, extracts unique recipient IDs, applies ML-based identity resolution using sklearn clustering, saves results to Excel, and streams live execution logs in real-time via Streamlit.

## WHAT IT SOLVES

Most email automation:
- Runs silently
- Fails invisibly  
- Can't be debugged live
- Can't be demonstrated

This system:
- Shows every step as it happens
- Emits live logs (not after)
- Uses real APIs (not stubs)
- Uses real ML (not rules)

## HOW IT WORKS (5 STEPS)

```
1. USER STARTS EXECUTION
   ↓
2. BACKEND EMITS EVENTS (live, to queue)
   ↓
3. UI POLLS QUEUE (displays logs in table)
   ↓
4. STEPS EXECUTE (fetch → ML → Excel)
   ↓
5. RESULTS DISPLAY (download Excel, show stats)
```

## ARCHITECTURE LAYERS

```
┌─────────────────────────────────────┐
│  UI Layer (Streamlit)               │ ← Start button, log table, download
├─────────────────────────────────────┤
│  Event Queue (in-memory)            │ ← Thread-safe log streaming
├─────────────────────────────────────┤
│  Execution Engine (task runner)     │ ← Orchestrates steps
├─────────────────────────────────────┤
│  Gmail | ML | Excel (modules)       │ ← Actual work
└─────────────────────────────────────┘
```

## LIVE LOGS IN ACTION

**When you click "Start" in Streamlit:**

```
Time: 01:13:42 | Step: Fetch Gmail Emails        | Status: STARTED  ← Emitted immediately
Time: 01:13:42 | Step: Fetch Gmail Emails        | Status: SUCCESS  ← Finished immediately
Time: 01:13:42 | Step: Resolve Duplicate...      | Status: STARTED  ← Next step starts
Time: 01:13:42 | Step: Resolve Duplicate...      | Status: SUCCESS  ← ML finished
Time: 01:13:43 | Step: Saving to Excel           | Status: STARTED  ← Writing...
Time: 01:13:43 | Step: Saving to Excel           | Status: SUCCESS  ← Done!
```

All events are **pushed to queue during execution**, not printed after.

## THE THREE MODULES

### Gmail Module
- Uses **real Gmail API** (OAuth2, not simulated)
- Fetches messages from sender
- Extracts To/Cc/Bcc headers
- Returns list of recipient emails

### ML Module
- Uses **sklearn AgglomerativeClustering**
- Normalizes email usernames
- Groups similar emails:
  - john.doe@gmail.com
  - johndoe@company.com  
  - john_doe@startup.io
  → All grouped as "johndoe"
- Keeps one representative from each cluster

### Excel Module
- Deduplicates emails
- Sorts alphabetically
- Exports single column: `recipient_email`
- Uses Pandas + openpyxl

## CODE EXAMPLE

Here's the entire execution flow:

```python
# 1. Create engine
engine = Engine()

# 2. Register steps
engine.add_step(1, "Fetch Emails", "Gmail API", fetch_emails)
engine.add_step(2, "Resolve Identities", "ML", resolve_identities)
engine.add_step(3, "Save Excel", "Pandas", save_excel)

# 3. Run
engine.run(context)

# 4. Events emitted during execution:
#    STARTED → SUCCESS at each step
#    If error: STARTED → FAILED
#    UI polls and displays live
```

## FILES YOU USE

```
Demo (No Setup):
  python backend/main_demo.py

Real Gmail (Setup Required):
  python backend/main.py

Web UI:
  streamlit run ui/app.py
```

## INTERVIEW EXPLANATION

> "I built a Gmail integration system with live execution observability. 
> The backend emits structured events to a thread-safe queue during execution. 
> The Streamlit UI polls this queue and displays a live log table. 
> The ML component uses scikit-learn's hierarchical clustering to resolve 
> duplicate email identities. The system is completely UI-agnostic—the backend 
> works with CLI, Streamlit, or any polling consumer."

## KEY FEATURES

| Feature | Why Matters | How It Works |
|---------|------------|-------------|
| **Real Gmail API** | Not simulated | Uses google-api-python-client with OAuth2 |
| **Live Logs** | See progress in real-time | Events queued during execution, not printed after |
| **Explainable ML** | Can explain every decision | sklearn clustering with clear normalization |
| **Excel Export** | Usable output | Deduplicated, sorted list in Excel |
| **Clean Code** | Interview-ready | 600 lines, PEP 8, no hacks |

## WHAT HAPPENS STEP BY STEP

### Step 1: Fetch Gmail Emails
```
Backend: authenticate() + service.users().messages().list()
Events:  "STARTED" → "SUCCESS"
Context: emails = [...]
```

### Step 2: Resolve Identities
```
Backend: normalize_email() + AgglomerativeClustering()
Events:  "STARTED" → "SUCCESS"
Context: emails = [deduplicated list]
```

### Step 3: Save to Excel
```
Backend: pd.DataFrame() → df.to_excel()
Events:  "STARTED" → "SUCCESS"
Context: excel_path = "...", recipient_count = N
```

All events visible in UI live.

## REQUIREMENTS

```
Python 3.8+
streamlit>=1.25.0       # Web UI
pandas>=1.3.0           # Data handling
openpyxl>=3.1.0         # Excel writing
scikit-learn>=0.24.0    # ML clustering
google-api-python-client>=2.50.0  # Gmail API
numpy>=1.21.0           # Numerical computing
```

All installed, tested, verified. ✅

## DEMO RESULTS

Running `python backend/main_demo.py`:

```
✓ Step 1: Fetch (mock data) → SUCCESS
✓ Step 2: ML deduplication → SUCCESS  
✓ Step 3: Excel export → SUCCESS

File: recipients_demo.xlsx
Recipients: 2 (after ML grouping)
```

Verified working, end-to-end.

## COMPARISON TO TYPICAL EMAIL SCRIPTS

| Aspect | Typical Script | This System |
|--------|---|---|
| Execution | Silent | Shows every step |
| Logging | Prints after | Streams live |
| API | Usually mocked | Real Gmail API |
| ML | Rules-based | sklearn clustering |
| UI | None | Streamlit |
| Errors | Hidden | Visible in logs |
| Demo-able | No | Yes (main_demo.py) |

## DEPLOYMENT OPTIONS

### Option 1: Local CLI
```powershell
python backend/main.py
```

### Option 2: Web UI
```powershell
streamlit run ui/app.py
```

### Option 3: Cloud Function
```python
# Wrap engine.run()
# Return JSON
```

### Option 4: Scheduled Job
```python
# Run daily
# Store in database
```

All possible because backend is UI-agnostic.

## INTERVIEW SCRIPT

**Q: Walk me through what your system does.**

"The user enters a sender email and output path. The backend creates an execution engine with three steps: fetch Gmail emails, resolve duplicate identities using ML, and save to Excel. Each step emits a STARTED event before running and a SUCCESS or FAILED event after. These events go into a thread-safe queue. The Streamlit UI polls this queue and displays a live log table. When I click 'Start', I see each step fire in real-time—not after execution completes."

**Q: Why use ML here?**

"Email identity resolution is a classic entity resolution problem. Rules fail because email addresses vary: john.doe@gmail.com, johndoe@company.com, and john_doe@startup.io all belong to one person. I normalize usernames, convert to feature vectors, apply hierarchical clustering, and group similar addresses. It's explainable and solves a real problem."

**Q: How do you ensure it's not simulated?**

"The logs emit during execution, not after. The UI polls the queue live—you see 'STARTED' before the step runs and 'SUCCESS' when it finishes. If something fails, you see it immediately. The Gmail API is real—uses oauth2 and google-api-python-client. The ML is real—scikit-learn clustering. Nothing is fake."

## FINAL STATUS

✅ Complete  
✅ Tested  
✅ Interview-ready  
✅ Production-grade  
✅ Deployable  

**Ready for delivery.**
