# Production Setup - CRITICAL FIX

## The Problem
Your OAuth redirect URI doesn't match. Google is rejecting the auth request.

## Fix (5 minutes)

### Step 1: Update Google Cloud Console
1. Go to https://console.cloud.google.com/
2. Select project: **gmail-intelligence-482221**
3. Go to **APIs & Services → Credentials**
4. Click your OAuth 2.0 Client ID (Desktop app)
5. Under **Authorized redirect URIs**, add exactly:
   ```
   http://localhost:8080/
   ```
6. Click **Save**

### Step 2: Download Updated Credentials
1. Click the OAuth client ID again
2. Download JSON (right side, download icon)
3. Replace: `backend/credentials.json`

### Step 3: Run Production
```powershell
cd c:\Users\Bimal Chakravarty\Divide\Documents\ML_submission\workcortex-gmail-intelligence
python run_production.py
```

That's it. The system will:
1. Ask for sender email
2. Ask for output path  
3. Open browser for OAuth
4. Fetch emails from Gmail
5. Apply ML deduplication
6. Save to Excel

## Current Credentials Status
✅ Client ID: 823617720210-f7jsn636u92r8ut11r7lsdbr7fre963p.apps.googleusercontent.com
❌ Redirect URI: NEEDS UPDATE (currently missing http://localhost:8080/)
✅ Gmail API: Enabled
✅ Scopes: gmail.readonly

## DO THIS NOW
Update the redirect URI in Google Cloud Console - that's the blocker.
