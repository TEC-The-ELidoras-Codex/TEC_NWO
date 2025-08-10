"""AI Expansion stub for ThoughtMap Phase 2.

Provides deterministic mock expansion until model integration (Azure OpenAI / local) is configured.
"""
from __future__ import annotations
from typing import List
import hashlib

SEED_TERMS = [
    "sovereignty", "architecture", "axiom alignment", "validation layer",
    "memory linkage", "narrative thread", "risk surface", "protocol hardening"
]

def expand_node(text: str, strategy: str = "concept", count: int = 4) -> List[str]:
    """Return a deterministic list of child concept suggestions.

    Args:
        text: Source node text/title.
        strategy: Expansion strategy (placeholder for future model prompt switch).
        count: Number of children to propose.
    """
    h = hashlib.sha256(f"{strategy}:{text}".encode()).hexdigest()
    indices = [int(h[i:i+2], 16) % len(SEED_TERMS) for i in range(0, 2*count, 2)]
    picks = []
    for idx, base in enumerate(indices):
        term = SEED_TERMS[base]
        picks.append(f"{term} – {text.split()[0]} pathway {idx+1}")
    return picks

def synthesize(children: List[str]) -> str:
    if not children:
        return "No children to synthesize yet."
    focus_terms = ", ".join(c.split(" – ")[0] for c in children[:5])
    return f"Synthesis focuses on: {focus_terms}."

if __name__ == "__main__":
    sample = expand_node("Guardian's Burden root doctrine")
    print("EXPAND SAMPLE:", sample)
    print("SYNTHESIS:", synthesize(sample))
