# TEC Datacore (Local RAG Bundle)

Quickstart

1. Create env

```powershell
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r tec_datacore/requirements.txt
copy tec_datacore/.env.example tec_datacore/.env
```

2. Ingest local files

```powershell
# Put docs under tec_datacore/data/raw then
python -m tec_datacore.ingest.pipeline
```

3. Serve RAG API

```powershell
uvicorn tec_datacore.server.rag_api:app --reload --port 8765
```

Notes

- Keep VECTOR_ROOT under repo for portability, or set to a separate drive.
- Optional integrations (Drive/GitHub/Gmail) are placeholders; wire credentials when ready.
- Optional reranker: set RERANK_ENABLE=true to blend vector and lexical scores (RapidFuzz). Tune RERANK_ALPHA (0..1) and RERANK_CAND_MULT (candidate multiplier) in .env.
