# server/rag_api.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from chromadb import PersistentClient

# Optional reranker via RapidFuzz
try:
    from rapidfuzz import process as rf_process, fuzz as rf_fuzz
except Exception:  # pragma: no cover - optional dependency at runtime
    rf_process = None  # type: ignore[assignment]
    rf_fuzz = None  # type: ignore[assignment]

DBPATH = os.getenv("VECTOR_ROOT", "./datastore/chroma")
client = PersistentClient(path=DBPATH)
coll = client.get_or_create_collection("tec")
app = FastAPI(title="TEC Datacore RAG API")

# Reranker toggles
RERANK_ENABLE = os.getenv("RERANK_ENABLE", "false").lower() == "true"
RERANK_ALPHA = float(os.getenv("RERANK_ALPHA", "0.5"))  # 0..1, weight for vector score
RERANK_CAND_MULT = max(1, int(os.getenv("RERANK_CAND_MULT", "3")))  # candidates = k * mult


class Query(BaseModel):
    q: str
    k: int = 8


@app.post("/search")
def search(q: Query):
    if not q.q.strip():
        return {"results": []}

    # Pull more candidates when reranking to let lexical score reshuffle
    n_results = q.k * RERANK_CAND_MULT if RERANK_ENABLE else q.k
    res = coll.query(
        query_texts=[q.q],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    ) or {}
    docs = (res.get("documents") or [[]])[0] or []
    metas = (res.get("metadatas") or [[]])[0] or []
    dists = (res.get("distances") or [[]])[0] or []

    # Base vector scores (higher is better)
    vec_scores = [float(1.0 / (1.0 + d)) if d is not None else 0.0 for d in dists]

    indices = list(range(len(docs)))

    # Optional reranking with RapidFuzz
    if RERANK_ENABLE and rf_process is not None and rf_fuzz is not None and len(docs) > 0:
        # Compute lexical similarity against the raw text chunks
        # Returns list of tuples: (doc, score, index)
        rf_results = rf_process.extract(q.q, docs, scorer=rf_fuzz.token_set_ratio, limit=len(docs))
        # Normalize to 0..1 scale
        rf_by_idx = {idx: (score / 100.0) for (_doc, score, idx) in rf_results}

        combined = []
        for i in indices:
            lex = rf_by_idx.get(i, 0.0)
            vec = vec_scores[i]
            final = (RERANK_ALPHA * vec) + ((1.0 - RERANK_ALPHA) * lex)
            combined.append((final, i))

        combined.sort(reverse=True, key=lambda x: x[0])
        top = combined[: q.k]
        out = []
        for score, i in top:
            meta = metas[i] if i < len(metas) else {}
            src = meta.get("source") if isinstance(meta, dict) else None
            out.append({"score": float(score), "source": src, "text": docs[i]})
        return {"results": out}

    # Default: return vector-order results
    out = []
    for doc, meta, score in zip(docs[: q.k], metas[: q.k], vec_scores[: q.k]):
        src = meta.get("source") if isinstance(meta, dict) else None
        out.append({"score": float(score), "source": src, "text": doc})
    return {"results": out}
