"""Embedding Service & RAG Utilities (Phase 1)

Generates embeddings (OpenAI) & provides similarity search + ThoughtMap ingestion.
"""
from __future__ import annotations
import os, hashlib
from typing import List, Sequence
import psycopg

try:
  from openai import OpenAI
except ImportError:  # pragma: no cover
  OpenAI = None  # type: ignore

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

def _get_openai_client():
  if OpenAI is None:
    raise RuntimeError("openai package not installed")
  api_key = os.getenv("OPENAI_API_KEY")
  if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing")
  return OpenAI(api_key=api_key)

def generate_embedding(text: str) -> List[float]:
  t = text.strip()
  if not t:
    return []
  client = _get_openai_client()
  resp = client.embeddings.create(input=[t], model=EMBED_MODEL)
  return resp.data[0].embedding  # type: ignore[attr-defined]

def db_conn():
  url = os.getenv("DATABASE_URL")
  if not url:
    raise RuntimeError("DATABASE_URL not set")
  return psycopg.connect(url, autocommit=True)

def _format_vector(vec: Sequence[float]) -> str:
  return "[" + ",".join(f"{v:.6f}" for v in vec) + "]"

def ensure_embedding(lore_entry_id: str, content: str, model: str = EMBED_MODEL) -> bool:
  if not content.strip():
    return False
  with db_conn() as conn, conn.cursor() as cur:
    cur.execute("SELECT id FROM \"Embedding\" WHERE \"loreEntryId\"=%s AND model=%s LIMIT 1", (lore_entry_id, model))
    if cur.fetchone():
      return False
    vec = generate_embedding(content)
    if not vec:
      return False
    cur.execute(
      "INSERT INTO \"Embedding\" (id, \"loreEntryId\", vector, model, dim, \"created_at\") VALUES (gen_random_uuid(), %s, %s::vector, %s, %s, NOW())",
      (lore_entry_id, _format_vector(vec), model, len(vec)),
    )
    return True

def similarity_search(query: str, k: int = 5) -> list[dict]:
  try:
    q_vec = generate_embedding(query)
    if not q_vec:
      return []
    with db_conn() as conn, conn.cursor() as cur:
      cur.execute(
        """
        SELECT l.id, l.slug, lv.content, (e.vector <=> %s::vector) AS distance
        FROM "Embedding" e
        JOIN "LoreEntry" l ON e."loreEntryId" = l.id
        JOIN "LoreVersion" lv ON lv."loreEntryId" = l.id
        ORDER BY e.vector <=> %s::vector
        LIMIT %s
        """,
        (_format_vector(q_vec), _format_vector(q_vec), k),
      )
      rows = cur.fetchall()
      return [{"lore_entry_id": r[0], "slug": r[1], "content": r[2], "distance": float(r[3])} for r in rows]
  except Exception:  # pragma: no cover
    return []

def ingest_thoughtmap(payload: dict) -> dict:
  title = payload.get("title") or "thoughtmap"
  nodes = payload.get("nodes") or []
  combined = "\n".join(n.get("text", "").strip() for n in nodes if n.get("text"))
  slug = _slugify(title)
  hashv = hashlib.sha256(combined.encode()).hexdigest()
  with db_conn() as conn, conn.cursor() as cur:
    cur.execute("SELECT id FROM \"LoreEntry\" WHERE slug=%s", (slug,))
    row = cur.fetchone()
    if row:
      lore_id = row[0]
    else:
      cur.execute(
        "INSERT INTO \"LoreEntry\" (id, slug, title, type, \"created_at\") VALUES (gen_random_uuid(), %s, %s, %s, NOW()) RETURNING id",
        (slug, title, "thoughtmap"),
      )
      lore_id = cur.fetchone()[0]
    cur.execute("SELECT id FROM \"LoreVersion\" WHERE \"loreEntryId\"=%s AND hash=%s", (lore_id, hashv))
    if not cur.fetchone():
      cur.execute(
        "INSERT INTO \"LoreVersion\" (id, \"loreEntryId\", content, author, hash, \"created_at\") VALUES (gen_random_uuid(), %s, %s, %s, %s, NOW())",
        (lore_id, combined, "system", hashv),
      )
    try:
      ensure_embedding(lore_id, combined)
    except Exception:
      pass
  return {"lore_entry_id": lore_id, "slug": slug, "hash": hashv, "nodes_ingested": len(nodes)}

def _slugify(text: str) -> str:
  return (text.lower().strip().replace(" ", "-")[:60].strip("-") or "thoughtmap")
