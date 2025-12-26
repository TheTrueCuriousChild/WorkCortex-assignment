Gmail API Setup (Quick)

1) Create a Google Cloud project
   - Go to: https://console.cloud.google.com/
   - Create or select a project

2) Enable Gmail API
   - APIs & Services -> Library -> search "Gmail API" -> Enable

3) Create OAuth credentials (Desktop app)
   - APIs & Services -> Credentials -> Create Credentials -> OAuth client ID
   - Application type: Desktop app
   - Download the JSON and save it as `credentials.json` in the project root

4) Alternate paths / placeholders
   - You can set environment variables instead of using `credentials.json` directly:
     - `GMAIL_CREDENTIALS_PATH` -> path to your client secrets JSON
     - `GMAIL_TOKEN_PATH` -> path where the token will be stored (default: `token.json`)

5) Placeholder file
   - A template `backend/credentials_placeholder.json` is included. Replace its values with your downloaded client secrets JSON.

Security note: Do NOT commit real credentials to source control. Keep `credentials.json` and `token.json` private.

If you'd like, paste the path to your `credentials.json` and I will verify authentication flow locally (you will still need to complete the OAuth consent in the browser).