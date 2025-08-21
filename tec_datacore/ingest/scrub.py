# ingest/scrub.py
import re
from typing import Iterable

EMAIL=re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE=re.compile(r"(?:(?:(?:\+?1)[ -]?)?(?:\(\d{3}\)|\d{3})[ -]?)?\d{3}[ -]?\d{4}")
KEYLIKE=re.compile(r"(?i)\b(sk-[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{20,})\b")

REDACT='[REDACTED]'

def pii_scrub(text: str) -> str:
    t = EMAIL.sub(REDACT, text)
    t = PHONE.sub(REDACT, t)
    t = KEYLIKE.sub(REDACT, t)
    return t
