"""
gmail.py - Gmail API Integration

Authenticates with Gmail API and fetches emails from a sender.
Uses OAuth2 (credentials.json from Google Cloud Console).
"""

import os
import re
# Optional DNS resolver for MX checks; imported lazily
try:
    import dns.resolver
    _HAS_DNS = True
except Exception:
    _HAS_DNS = False
import pickle
from email.utils import getaddresses
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Simple email validation regex (pragmatic, not full RFC)
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def authenticate():
    """
    Authenticate with Gmail API using OAuth2.
    
    First run: Opens browser for user consent
    Subsequent runs: Uses saved token.json
    
    Returns:
        Authenticated Gmail service
    """
    creds = None
    
    # Get the backend directory path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Support custom paths via environment variables, else use backend directory
    cred_path = os.environ.get("GMAIL_CREDENTIALS_PATH", os.path.join(backend_dir, "credentials.json"))
    token_path = os.environ.get("GMAIL_TOKEN_PATH", os.path.join(backend_dir, "token.json"))

    # Load existing token if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES
            )
            # Use specific port for OAuth callback
            creds = flow.run_local_server(port=8080, open_browser=True)
        
        # Save token for next time
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)


def fetch_emails(context):
    """
    Fetch all emails from a specific sender.
    
    Args:
        context: Execution context dict
            Must contain: sender
            Will populate: emails (list of recipient emails)
    
    Raises:
        Exception: If Gmail API call fails
    """
    sender = context.get("sender")
    if not sender:
        raise ValueError("sender not provided in context")
    
    try:
        service = authenticate()
        
        # Get authenticated user's email address (for logging, not filtering)
        try:
            profile = service.users().getProfile(userId="me").execute()
            auth_email = profile.get("emailAddress")
            context["receiver"] = auth_email
        except Exception:
            context["receiver"] = None

        # Query for ALL emails from sender (regardless of recipient)
        # This fetches all emails the sender sent (to anyone in the authenticated user's mailbox)
        query = f"from:{sender}"
        
        print(f"\n[DEBUG] Searching Gmail with query: {query}")

        # Handle pagination - collect all messages matching the query
        messages = []
        request = service.users().messages().list(userId="me", q=query)
        while request is not None:
            resp = request.execute()
            msgs = resp.get("messages", [])
            if msgs:
                messages.extend(msgs)
            # Get next page, if any
            request = service.users().messages().list_next(request, resp)

        print(f"[DEBUG] Found {len(messages)} messages from {sender}")

        if not messages:
            print(f"[DEBUG] No messages found - returning empty emails list")
            context["emails"] = []
            return

        recipients = []

        # Extract recipients from each message
        for msg in messages:
            try:
                data = service.users().messages().get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["To", "Cc", "Bcc"]
                ).execute()
                
                headers = data.get("payload", {}).get("headers", [])
                
                for header in headers:
                    if header["name"] in ["To", "Cc", "Bcc"]:
                        # Use getaddresses to reliably parse lists like "Name <a@b.com>, c@d.com"
                        parsed = getaddresses([header.get("value", "")])
                        for _name, addr in parsed:
                            addr = addr.strip()
                            if not addr:
                                continue
                            # Validate email format
                            if EMAIL_REGEX.match(addr):
                                recipients.append(addr)
                            else:
                                # skip malformed addresses
                                continue
            
            except Exception as e:
                # Log but continue
                print(f"Warning: Could not parse message {msg['id']}: {e}")
                continue
        
        # Exclude the authenticated user's email from recipients (we want external recipients)
        filtered = [r for r in recipients if r.lower() != auth_email.lower()] if auth_email else recipients

        print(f"[DEBUG] Extracted {len(recipients)} total recipients, {len(filtered)} after filtering auth email")
        print(f"[DEBUG] Recipients: {filtered[:10]}")  # First 10 for debugging

        # If requested, verify domains via MX lookup
        verify_mx = context.get("verify_mx", False)
        verification_failures = []

        if verify_mx and _HAS_DNS:
            validated = []
            for addr in filtered:
                domain = addr.split("@")[-1]
                try:
                    answers = dns.resolver.resolve(domain, 'MX')
                    if answers:
                        validated.append(addr)
                    else:
                        verification_failures.append(addr)
                except Exception:
                    verification_failures.append(addr)

            context["emails"] = validated
            context["verification_failures"] = verification_failures
            print(f"[DEBUG] After MX verification: {len(validated)} valid, {len(verification_failures)} failed")
        else:
            context["emails"] = filtered
            print(f"[DEBUG] Final emails list: {len(filtered)} recipients")
    
    except Exception as e:
        raise Exception(f"Gmail API error: {str(e)}")

