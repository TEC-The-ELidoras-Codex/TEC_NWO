import json
import time
from pathlib import Path
from typing import Any, Dict


def write_provenance(dir_path: Path, tool: str, version: str, inputs: Dict[str, Any], cost_estimate: float | None = None) -> Path:
    dir_path.mkdir(parents=True, exist_ok=True)
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    payload = {
        "tool": tool,
        "version": version,
        "inputs": inputs,
        "started_at": now,
        "finished_at": now,
    }
    if cost_estimate is not None:
        payload["cost_estimate"] = cost_estimate
    out = dir_path / "provenance.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out
