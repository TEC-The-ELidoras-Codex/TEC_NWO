"""Backfill embeddings for LoreEntries without embeddings for chosen model."""
from __future__ import annotations
import argparse
from services.airth.embedding_service import db_conn, ensure_embedding

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--model", default="text-embedding-3-small")
  args = parser.parse_args()
  created = 0
  with db_conn() as conn, conn.cursor() as cur:
    cur.execute(
      """
      SELECT l.id, lv.content
      FROM "LoreEntry" l
      JOIN "LoreVersion" lv ON lv."loreEntryId" = l.id
      LEFT JOIN "Embedding" e ON e."loreEntryId" = l.id AND e.model = %s
      WHERE e.id IS NULL
      """,
      (args.model,),
    )
    rows = cur.fetchall()
  for lore_id, content in rows:
    if ensure_embedding(lore_id, content, args.model):
      created += 1
  print(f"Embeddings created: {created}")
  return 0

if __name__ == "__main__":  # pragma: no cover
  import sys
  raise SystemExit(main())
