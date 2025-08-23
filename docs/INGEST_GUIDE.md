# Ingestion Guide (What to download, where to put it)

Where to put files

- Drop source files to analyze under `tec_datacore/data/raw/`.
- Use subfolders to tag categories (optional):
  - `tec_datacore/data/raw/research/` for saved articles (.html, .md, .txt, .pdf)
  - `tec_datacore/data/raw/scripts/` for drafts and outlines (.md, .docx)
  - `tec_datacore/data/raw/transcripts/` for text transcripts (.txt)

Supported formats

- Text: .md, .txt, .json
- Documents: .pdf, .docx, .rtf (rtf best saved as .docx)
- Web pages: .html (saved page), basic tag stripping applied

How to index

1) Create and activate a venv, then install deps

```powershell
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r tec_datacore/requirements.txt
copy tec_datacore/.env.example tec_datacore/.env
```

2) Ingest

```powershell
# Put files under tec_datacore/data/raw then run:
python -m tec_datacore.ingest.pipeline
```

3) Query (optional local API)

```powershell
uvicorn tec_datacore.server.rag_api:app --port 8765
```

Notes

- The script `tools/ops/pull_from_drive.ps1` can curate-copy from Drive into `tec_datacore/data/raw/research` with a dry-run report by default. Use `-Execute` to copy.
- Metadata tags include `project` and `category` based on the path layout; use folders to organize.
