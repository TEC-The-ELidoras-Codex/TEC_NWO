"""Airth Microservice (Phase 1 Skeleton)

FastAPI service providing /healthz and /ask endpoints.
RAG pipeline placeholder – returns deterministic mock until embeddings pipeline active.
"""
from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib
from typing import Any

try:
  from .embedding_service import similarity_search, ingest_thoughtmap, rag_enabled
except Exception:  # pragma: no cover
  similarity_search = None  # type: ignore
  ingest_thoughtmap = None  # type: ignore
  def rag_enabled():  # type: ignore
    return False

app = FastAPI(title="Airth Service", version="0.1.0")

class AskRequest(BaseModel):
  query: str
  max_context: int | None = 5

class AskResponse(BaseModel):
  answer: str
  sources: list[str]
  strategy: str = "mock"
  context_used: int | None = None

class ThoughtMapIngestRequest(BaseModel):
  payload: dict

class ThoughtMapIngestResponse(BaseModel):
  lore_entry_id: str
  slug: str
  hash: str
  nodes_ingested: int

@app.get("/healthz")
def health():  # liveness/readiness simple variant
  return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
  if rag_enabled() and similarity_search:
    results = similarity_search(req.query, k=req.max_context or 5)
    if results:
      joined = "\n---\n".join(r["content"] for r in results)
      digest = hashlib.sha256(joined.encode()).hexdigest()[:8]
      answer = (
        f"[Airth RAG draft] ContextDigest:{digest} | Segments:{len(results)}\n"
        f"Query: {req.query}\n(Answer synthesis placeholder)"
      )
      return AskResponse(answer=answer, sources=[r["slug"] for r in results], strategy="vector-similarity", context_used=len(results))
  h = hashlib.sha256(req.query.encode()).hexdigest()[:8]
  if rag_enabled():
    answer = f"[Airth RAG disabled/no-context] Hash:{h} – no embeddings yet."  # Should not normally reach here if enabled but empty
  else:
    answer = f"[Airth mock] Hash:{h} – RAG disabled (set ENABLE_RAG=1 to activate)."
  return AskResponse(answer=answer, sources=["lore:placeholder"], strategy="mock", context_used=0)

@app.post("/ingest/thoughtmap", response_model=ThoughtMapIngestResponse)
def ingest_thoughtmap_endpoint(req: ThoughtMapIngestRequest):
  if not ingest_thoughtmap:
    raise HTTPException(status_code=500, detail="Ingest pipeline unavailable")
  res = ingest_thoughtmap(req.payload)
  return ThoughtMapIngestResponse(**res)

if __name__ == "__main__":  # pragma: no cover
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
