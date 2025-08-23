# TEC Agent Orchestration (Local)

This folder hosts a minimal local agent service that:

- exposes a small HTTP API (OpenAPI) for ChatGPT “Actions” / tools
- bridges to your local MCP Datacore (datacore_search)
- logs runs and emits provenance for artifacts

## Components

- server.py — FastAPI service exposing /search, /plan, /run
- openapi.yaml — machine-readable API for ChatGPT Actions integration
- provenance.py — helper for per-call provenance.json
- requirements.txt — pinned deps

## Quickstart

1. Create venv and install deps

    ```powershell
    python -m venv .venv
    . .\.venv\Scripts\Activate.ps1
    pip install -r orchestration/requirements.txt
    ```

1. Configure environment

    ```powershell
    $env:DATACORE_URL = "http://127.0.0.1:8765/search"
    $env:PORT = "8787"
    ```

1. Run locally

    ```powershell
    python -m orchestration.server
    ```

1. Connect from ChatGPT (Actions)

    - In ChatGPT, create a custom action and upload `orchestration/openapi.yaml`.
    - Set the base URL to `http://localhost:8787` (or your tunnel URL if remote).

## Notes

- This is a minimal bridge; expand with more tools as you wire agents.
- Keep secrets out of the spec. Use environment variables only.
