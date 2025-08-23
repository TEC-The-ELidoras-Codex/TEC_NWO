# TEC — Recap and Next Steps (Snapshot)

This snapshot captures the current state and the minimal daily loop.

What’s in place
- Datacore RAG (local Chroma) with HTML/MD/PDF/DOCX ingestion and path-based metadata tags.
- Cost-safe embeddings: local fallback (MODEL_EMBED=local) to avoid network spend.
- MCP/Agent wiring stubs and a REST RAG API server.
- Drive hygiene: clean_research.ps1 (purges *_files + web junk) and pull_from_drive.ps1 (curated copy, report-first).
- Ignore rules set for large or transient artifacts.

Daily loop
1) Save articles into tec_datacore/data/raw/research.
2) Run tools/ops/clean_research.ps1 (preview; then -Execute if needed).
3) Run tools/ops/pull_from_drive.ps1 -Execute to consolidate.
4) Ingest: python -m tec_datacore.ingest.pipeline (MODEL_EMBED=local for zero-cost).
5) Optional: serve search API (uvicorn tec_datacore.server.rag_api:app --port 8765).

Notes
- Vector DB lives under tec_datacore/datastore/chroma and is gitignored.
- SQL/Postgres is optional and not required for local flow.

Next steps
- Add a VS Code task that runs clean → pull → ingest in sequence.
- Optional: add RapidFuzz reranker and MCP tool entries for direct IDE search.
