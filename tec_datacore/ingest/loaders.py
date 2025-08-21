# ingest/loaders.py
from pathlib import Path
from pypdf import PdfReader
import docx, re, io
from markdown_it import MarkdownIt

def load_fs(path: Path, patterns):
    for pat in patterns:
        for p in path.rglob(pat):
            yield str(p), p.read_bytes()

def read_pdf(b: bytes)->str:
    pdf = PdfReader(io.BytesIO(b))
    return "\n".join((p.extract_text() or "") for p in pdf.pages)

def read_docx(b: bytes)->str:
    f = io.BytesIO(b)
    d = docx.Document(f)
    return "\n".join(p.text for p in d.paragraphs)

def read_md(b: bytes)->str:
    txt = b.decode("utf-8",errors="ignore")
    html = MarkdownIt().render(txt)
    return re.sub("<[^>]+>"," ", html)

def sniff_and_text(name: str, b: bytes)->str:
    n = name.lower()
    if n.endswith(".pdf"): return read_pdf(b)
    if n.endswith(".docx"): return read_docx(b)
    if n.endswith(".md"): return read_md(b)
    if n.endswith(".txt") or n.endswith(".json"): return b.decode("utf-8",errors="ignore")
    return ""
