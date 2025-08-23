import os
from pathlib import Path
from typing import List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

try:
    from orchestration.provenance import write_provenance
except Exception:  # pragma: no cover
    # Fallback when running as a script without package context
    from provenance import write_provenance  # type: ignore

APP_VERSION = "0.1.0"
ARTIFACT_ROOT = Path("artifacts")

app = FastAPI(title="TEC Agent Bridge", version=APP_VERSION)


class SearchRequest(BaseModel):
    q: str = Field(..., description="Query text")
    k: int = Field(8, ge=1, le=50, description="Top-k results")


class SearchResult(BaseModel):
    query: str
    results: List[dict]


class PlanRequest(BaseModel):
    goal: str = Field(..., description="High-level objective")


class PlanResponse(BaseModel):
    steps: List[str]


class HealthResponse(BaseModel):
    status: str
    version: str
    datacore_url: Optional[str] = None


@app.post("/search", response_model=SearchResult)
async def search(req: SearchRequest) -> SearchResult:
    datacore_url = os.environ.get("DATACORE_URL", "http://127.0.0.1:8765/search")
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            r = await client.post(datacore_url, json={"q": req.q, "k": req.k})
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Datacore error: {e}")
    run_dir = ARTIFACT_ROOT / "search"
    write_provenance(run_dir, tool="datacore_search", version=APP_VERSION, inputs=req.dict())
    return SearchResult(query=req.q, results=data.get("results") or data)


@app.post("/plan", response_model=PlanResponse)
async def plan(req: PlanRequest) -> PlanResponse:
    # Minimal stub: expand later to produce agent graphs
    steps = [
        "continuity: pull citations via datacore_search",
        "script: draft beats with tags",
        "visuals: request concept frames",
        "audio: request cues",
    ]
    run_dir = ARTIFACT_ROOT / "plan"
    write_provenance(run_dir, tool="planner", version=APP_VERSION, inputs=req.dict())
    return PlanResponse(steps=steps)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=APP_VERSION, datacore_url=os.environ.get("DATACORE_URL"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8787"))
    uvicorn.run("orchestration.server:app", host="0.0.0.0", port=port, reload=False)
