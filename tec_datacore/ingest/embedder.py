"""Embedding helpers with cost-safe local fallback.

Default uses OpenAI embeddings when OPENAI_API_KEY is present and MODEL_EMBED
is not set to 'local'. If no key is set or MODEL_EMBED=local, a deterministic
hash-based embedding is used to avoid network calls and costs.
"""

import os
import math
import hashlib
from typing import List

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - OpenAI not required for local mode
    OpenAI = None  # type: ignore

_client = None

def _client_openai():
    global _client
    if OpenAI is None:
        raise RuntimeError("openai package not available; set MODEL_EMBED=local or install dependencies")
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def _embed_local(texts: List[str], dim: int = 384) -> List[List[float]]:
    """Deterministic hash embedding: fast, no network, stable.

    We map unicode codepoints and 3-grams into a fixed-size bag-of-hashes vector
    and L2-normalize. This isn't semantically rich but is decent for local smoke tests.
    """
    out: List[List[float]] = []
    for t in texts:
        vec = [0.0] * dim
        s = t or ""
        # character-level contribution
        for ch in s:
            h = int(hashlib.sha1(ch.encode("utf-8")).hexdigest(), 16)
            idx = h % dim
            vec[idx] += 1.0
        # 3-gram contribution
        for i in range(max(0, len(s) - 2)):
            tri = s[i:i+3]
            h = int(hashlib.md5(tri.encode("utf-8")).hexdigest(), 16)
            idx = h % dim
            vec[idx] += 2.0
        # normalize
        norm = math.sqrt(sum(v*v for v in vec)) or 1.0
        out.append([v / norm for v in vec])
    return out

def embed(texts: List[str], model: str | None = None) -> List[List[float]]:
    if not texts:
        return []
    model = model or os.getenv("MODEL_EMBED")
    use_local = (model or "").lower() == "local" or not os.getenv("OPENAI_API_KEY")
    if use_local:
        return _embed_local(texts)

    # Default to OpenAI if available and not explicitly local
    model_name = model or "text-embedding-3-large"
    client = _client_openai()
    vecs: List[List[float]] = []
    for i in range(0, len(texts), 128):
        batch = texts[i:i+128]
        res = client.embeddings.create(model=model_name, input=batch)
        vecs.extend([d.embedding for d in res.data])
    return vecs
