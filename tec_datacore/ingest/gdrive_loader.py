from __future__ import annotations
import os, io
from typing import Iterable, Tuple
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def _svc():
    creds_path = os.getenv("GDRIVE_CREDS_JSON")
    if not creds_path:
        return None
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds, cache_discovery=False)

def list_docs_by_names(includes: list[str], max_files: int = 200) -> Iterable[Tuple[str, bytes]]:
    svc = _svc()
    if not svc:
        return []
    q = " or ".join([f"name contains '{w}'" for w in includes]) or "trashed = false"
    res = svc.files().list(q=q, fields="files(id,name,mimeType)", pageSize=max_files).execute()
    files = res.get('files', [])
    for f in files:
        fid, name, mt = f['id'], f['name'], f.get('mimeType','')
        try:
            if mt.startswith('application/vnd.google-apps.document'):
                data = svc.files().export(fileId=fid, mimeType='text/plain').execute()
                if not isinstance(data, bytes):
                    data = bytes(data or b"")
                yield name+".txt", data
            else:
                req = svc.files().get_media(fileId=fid)
                buf = io.BytesIO()
                from googleapiclient.http import MediaIoBaseDownload
                downloader = MediaIoBaseDownload(buf, req)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                yield name, buf.getvalue()
        except Exception:
            continue
