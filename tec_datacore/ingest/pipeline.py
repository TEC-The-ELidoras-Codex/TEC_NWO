Get-ChildItem -Force tec_datacore\datastore -ErrorAction SilentlyContinue | Format-Table -AutoSize# ingest/pipeline.py
import os
import yaml
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from chromadb import PersistentClient
from typing import Sequence
import fnmatch
import numpy as np

from tec_datacore.ingest.loaders import load_fs, sniff_and_text
from tec_datacore.ingest.chunkers import chunk_text
from tec_datacore.ingest.embedder import embed
from tec_datacore.ingest.scrub import pii_scrub
from tec_datacore.ingest.github_loader import list_repo_files
from tec_datacore.ingest.gdrive_loader import list_docs_by_names
from tec_datacore.ingest.gmail_loader import list_messages_snippets

load_dotenv()
# Resolve config relative to this file unless overridden by INGEST_CONFIG
_default_cfg_path = Path(__file__).resolve().parent / "config.yaml"
cfg_path = Path(os.getenv("INGEST_CONFIG", str(_default_cfg_path)))
cfg = yaml.safe_load(cfg_path.read_text())

DBPATH = os.getenv("VECTOR_ROOT","./datastore/chroma")
client = PersistentClient(path=DBPATH)
coll = client.get_or_create_collection("tec")
PKG_ROOT = Path(__file__).resolve().parents[1]
RAW_ROOT = (PKG_ROOT / "data" / "raw").resolve()
PROJECT_NAME = os.getenv("PROJECT_NAME", "TEC_NWO")

BLOCKLIST = [g.strip() for g in os.getenv("BLOCKLIST_GLOBS","**/secrets/**,**/*.key,**/.env").split(',') if g.strip()]
SCRUB = os.getenv("SCRUB_PII","true").lower() in ("1","true","yes")

def blocked(path: str) -> bool:
    for pat in BLOCKLIST:
        if fnmatch.fnmatch(path, pat):
            return True
    return False

def doc_id(s: str)->str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()

def path_category(name: str) -> str:
    try:
        p = Path(name).resolve()
        rel = p.relative_to(RAW_ROOT)
        parts = rel.parts
        return parts[0] if len(parts) > 1 else "misc"
    except Exception:
        return "misc"

def ingest_fs():
    for src in cfg.get("sources", []):
        if src.get("type") == "fs":
            # Allow relative paths in config to be relative to tec_datacore package root
            base = (PKG_ROOT / src["path"]).resolve() if not Path(src["path"]).is_absolute() else Path(src["path"]).resolve()
            patterns = src.get("patterns", ["**/*.md","**/*.txt"])
            for name, b in load_fs(base, patterns):
                if blocked(name):
                    continue
                txt = sniff_and_text(name, b)
                if not txt.strip():
                    continue
                if SCRUB:
                    txt = pii_scrub(txt)
                chunks = chunk_text(txt)
                if not chunks:
                    continue
                ids = [doc_id(name+f"#{k}") for k,_ in enumerate(chunks)]
                embs_list = embed(chunks)
                embs = np.array(embs_list, dtype=np.float32)
                cat = path_category(name)
                metas = [{"source": name, "project": PROJECT_NAME, "category": cat} for _ in chunks]
                coll.upsert(documents=chunks, embeddings=embs, metadatas=metas, ids=ids)  # type: ignore[arg-type]
    # optional: transcripts folder
    tdir = Path(os.getenv("DATA_ROOT","./data")).joinpath("transcripts")
    if tdir.exists():
        for p in tdir.rglob("*.txt"):
            name = str(p)
            if blocked(name):
                continue
            txt = p.read_text(encoding="utf-8", errors="ignore")
            if not txt.strip():
                continue
            if SCRUB:
                txt = pii_scrub(txt)
            chunks = chunk_text(txt)
            if not chunks:
                continue
            ids = [doc_id(name+f"#{k}") for k,_ in enumerate(chunks)]
            embs_list = embed(chunks)
            embs = np.array(embs_list, dtype=np.float32)
            cat = path_category(name)
            metas = [{"source": name, "project": PROJECT_NAME, "category": cat} for _ in chunks]
            coll.upsert(documents=chunks, embeddings=embs, metadatas=metas, ids=ids)  # type: ignore[arg-type]

def ingest_github():
    if os.getenv("GITHUB_ENABLE","false").lower() not in ("1","true","yes"):
        return
    repo = os.getenv("GITHUB_REPO","TEC-The-ELidoras-Codex/TEC_NWO")
    globs = [g.strip() for g in os.getenv("GITHUB_GLOBS","**/*.md,**/*.json,**/*.py").split(',') if g.strip()]
    for name, b in list_repo_files(repo, globs):
        if blocked(name):
            continue
        txt = sniff_and_text(name, b)
        if not txt.strip():
            continue
        if SCRUB:
            txt = pii_scrub(txt)
        chunks = chunk_text(txt)
        if not chunks:
            continue
        ids = [doc_id(name+f"#{k}") for k,_ in enumerate(chunks)]
        embs = np.array(embed(chunks), dtype=np.float32)
        cat = path_category(name)
        metas = [{"source": name, "project": PROJECT_NAME, "category": cat} for _ in chunks]
        coll.upsert(documents=chunks, embeddings=embs, metadatas=metas, ids=ids)  # type: ignore[arg-type]

def ingest_gdrive():
    if os.getenv("GDRIVE_ENABLE","false").lower() not in ("1","true","yes"):
        return
    includes = [w.strip() for w in os.getenv("GDRIVE_INCLUDE","TEC,Elidoras").split(',') if w.strip()]
    for name, b in list_docs_by_names(includes):
        if blocked(name):
            continue
        txt = sniff_and_text(name, b)
        if not txt.strip():
            continue
        if SCRUB:
            txt = pii_scrub(txt)
        chunks = chunk_text(txt)
        if not chunks:
            continue
        ids = [doc_id(name+f"#{k}") for k,_ in enumerate(chunks)]
        embs = np.array(embed(chunks), dtype=np.float32)
        cat = path_category(name)
        metas = [{"source": name, "project": PROJECT_NAME, "category": cat} for _ in chunks]
        coll.upsert(documents=chunks, embeddings=embs, metadatas=metas, ids=ids)  # type: ignore[arg-type]

def ingest_gmail():
    if os.getenv("GMAIL_ENABLE","false").lower() not in ("1","true","yes"):
        return
    query = os.getenv("GMAIL_QUERY","label:TEC OR subject:(TEC OR Elidoras)")
    for name, b in list_messages_snippets(query):
        if blocked(name):
            continue
        txt = b.decode('utf-8','ignore')
        if not txt.strip():
            continue
        if SCRUB:
            txt = pii_scrub(txt)
        chunks = chunk_text(txt)
        if not chunks:
            continue
        ids = [doc_id(name+f"#{k}") for k,_ in enumerate(chunks)]
        embs = np.array(embed(chunks), dtype=np.float32)
        metas = [{"source": name} for _ in chunks]
        coll.upsert(documents=chunks, embeddings=embs, metadatas=metas, ids=ids)  # type: ignore[arg-type]

if __name__ == "__main__":
    ingest_fs()
    ingest_github()
    ingest_gdrive()
    ingest_gmail()
    print("✅ Ingest complete →", coll.count(), "chunks")
