Next Session Kickoff Prompt

- Goal: Index any new research and validate search.
- Actions for Copilot:
  1) Run tools/ops/clean_research.ps1 -Source "TEC-HORRORMASTERCLASS/TEC-Research" (preview), then -Execute if items are listed.
  2) Run tools/ops/pull_from_drive.ps1 -Source "TEC-HORRORMASTERCLASS/TEC-Research" -Execute.
  3) Set MODEL_EMBED=local and run python -m tec_datacore.ingest.pipeline.
  4) Start uvicorn tec_datacore.server.rag_api:app --port 8765 and perform one smoke /search.
  5) Summarize deltas: docs ingested count, any errors, and top 3 sources by size.
