# ingest/chunkers.py
import os
import tiktoken
from typing import Optional, List

def chunk_text(text: str, model: Optional[str] = None, chunk_tokens: Optional[int] = None, overlap: Optional[int] = None) -> List[str]:
    model = model or os.getenv("MODEL_EMBED", "text-embedding-3-large")
    chunk_tokens = chunk_tokens or int(os.getenv("CHUNK_TOKENS", "800"))
    overlap = overlap or int(os.getenv("CHUNK_OVERLAP", "120"))
    enc = tiktoken.encoding_for_model("gpt-4o-mini")
    toks = enc.encode(text)
    out: List[str] = []
    i = 0
    while i < len(toks):
        j = min(i + chunk_tokens, len(toks))
        out.append(enc.decode(toks[i:j]))
        i = j - overlap
        if i < 0:
            i = 0
    return [c.strip() for c in out if c.strip()]
