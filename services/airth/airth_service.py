"""Airth Microservice (Phase 1 Skeleton)

FastAPI service providing /healthz and /ask endpoints.
RAG pipeline placeholder – returns deterministic mock until embeddings pipeline active.
"""
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI(title="Airth Service", version="0.1.0")

class AskRequest(BaseModel):
  query: str
  max_context: int | None = 5

class AskResponse(BaseModel):
  answer: str
  sources: list[str]
  strategy: str = "mock"

@app.get("/healthz")
def health():  # liveness/readiness simple variant
  return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
  h = hashlib.sha256(req.query.encode()).hexdigest()[:8]
  answer = f"[Airth mock] Hash:{h} – query acknowledged. RAG pipeline pending."
  return AskResponse(answer=answer, sources=["lore:placeholder"], strategy="mock")

if __name__ == "__main__":  # pragma: no cover
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
