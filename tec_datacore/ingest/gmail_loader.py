from __future__ import annotations
import os, base64
from typing import Iterable, Tuple
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def _svc():
    token_path = os.getenv("GMAIL_TOKEN_JSON")
    if not token_path:
        return None
    creds = Credentials.from_authorized_user_file(token_path, scopes=SCOPES)
    return build('gmail', 'v1', credentials=creds, cache_discovery=False)

def list_messages_snippets(query: str, max_results: int = 50) -> Iterable[Tuple[str, bytes]]:
    svc = _svc()
    if not svc:
        return []
    msgs = svc.users().messages().list(userId='me', q=query, maxResults=max_results).execute().get('messages', [])
    for m in msgs:
        try:
            full = svc.users().messages().get(userId='me', id=m['id'], format='full').execute()
            subject = ""
            for h in full.get('payload',{}).get('headers',[]):
                if h.get('name','').lower() == 'subject':
                    subject = h.get('value','')
                    break
            body_text = full.get('snippet','')
            parts = full.get('payload',{}).get('parts',[]) or []
            for p in parts:
                if p.get('mimeType') == 'text/plain':
                    body_data = p.get('body',{}).get('data')
                    if body_data:
                        body_text = base64.urlsafe_b64decode(body_data).decode('utf-8', 'ignore')
                        break
            name = f"gmail:{subject[:80]}"
            yield name, body_text.encode('utf-8')
        except Exception:
            continue
