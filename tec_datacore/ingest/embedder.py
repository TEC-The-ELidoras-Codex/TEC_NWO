# ingest/embedder.py
import os
from typing import List
from openai import OpenAI

_client = None

def _client_openai():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def embed(texts: List[str], model: str = None) -> List[List[float]]:
    model = model or os.getenv("MODEL_EMBED", "text-embedding-3-large")
    if not texts:
        return []
    client = _client_openai()
    vecs: List[List[float]] = []
    for i in range(0, len(texts), 128):
        batch = texts[i:i+128]
        res = client.embeddings.create(model=model, input=batch)
        vecs.extend([d.embedding for d in res.data])
    return vecs
