# TEC Multi‑Agent Creative System (Copilot Playbook)

Purpose

- Give Copilot and automation agents a clear contract to build TEC content end‑to‑end (scripts → visuals → voices → score), with observability and ethical guardrails.
- Keep costs and complexity controllable; prefer local, reproducible stacks first.

Scope

- Narrative pipelines (script, adaptation, continuity)
- Visual generation (concepts, keyframes, 3D prep)
- Casting and voice (avatars, timbre, timing)
- Audio (music cues, SFX stems, mix)
- Orchestration, observability, and permissions

## Core agents and contracts

For each agent, follow a simple contract: inputs, outputs, tools, success, failure.

1. Story Architect

- Inputs: TEC lore docs, outline/theme prompts, continuity constraints, “don’t break canon” list
- Outputs: scene list, script pages (Fountain/Markdown), beat map with tags (hope, fracture, rite)
- Tools: Local Datacore search (MCP tool: datacore_search), embedding notes, outline templates
- Success: Script passes axiom validation, continuity checks, and tone targets
- Failure: Canon violations, unsupported claims, or missing beat tags

1. Visual Engineer

- Inputs: scene list + key descriptions + style bible
- Outputs: concept frames (PNG/WebP), shot boards, optional Blender scene stubs
- Tools: Diffusion pipeline (Stable Diffusion/ComfyUI), Blender CLI (optional), palette generator
- Success: Frames match tags (ritual, entropy, prison logic), character silhouettes consistent
- Failure: Inconsistent palette or character form; missing frames for required beats

1. Casting Synth

- Inputs: character bios, accent/emotion notes, dialogue
- Outputs: voice takes (wav), viseme timing, basic avatar rig or reference pack
- Tools: TTS/voice APIs (toggle via env), phoneme aligner, lip‑sync data
- Success: Intelligible, consistent timbre; timing metadata emitted
- Failure: Drift in voice identity; missing timing marks

1. Audio Composer

- Inputs: script beats + emotion curve + temp SFX list
- Outputs: stems (music/SFX/VO bus), cue sheet, mix notes
- Tools: Local generative audio, sampler kit, DAW macros (optional CLI)
- Success: Cues reinforce beats; clean separation of stems
- Failure: Masking dialogue; missing hits for jumps/rites

## Orchestration

- Coordinator: LangGraph/Crew‑style graph with explicit steps; each step writes artifacts to /artifacts/{runId}/{phase}
- Memory: Vector notes in local Datacore (Chroma) keyed by project/run
- MCP: Expose datacore_search to all agents (already added); prefer local tools first
- Idempotency: Steps can resume from last green artifact; hash inputs to skip redundant work

## Observability (“show me what it’s doing”)

- Run log: JSONL per run with step, start/stop, inputs hash, artifact URIs
- Web actions: When browsing is needed, use a headless browser with:
  - Snapshots per navigation (PNG)
  - HAR capture (network)
  - Console log tee → /artifacts/{runId}/web/
- Provenance: Each artifact carries a provenance.json (tool, version, params, time)

Minimal schema: provenance.json

- tool: string
- version: string
- inputs: object
- started_at / finished_at: ISO timestamps
- cost_estimate: number (optional)

## Permissions and safety

- Tool gating: Env toggles per external API; default off
- Dry‑run mode: generate plans and file trees without hitting network
- Secrets via .env or vault; never hard‑code
- Axiom validation required for public/canonical outputs

## Cost controls

- Prefer local models/tooling; batch external calls; cache aggressively
- Emit cost_estimate in provenance when APIs are used

## Web “with power” (controlled surf)

- Browser: Playwright/Chromium in a sandboxed profile
- Actions: navigate, click, type, download (to artifacts), screenshot; record MP4 if needed
- Telemetry: Save DOM snapshots (optional), console, network
- Ethics: Respect robots/no‑scrape; add user agent identifying TEC research

## Getting started checklist

- [ ] Create /artifacts/ (gitignored) for runs
- [ ] Wire MCP client calls to datacore_search for continuity pulls
- [ ] Add run log writer and provenance helper (small Python util)
- [ ] Pick diffusion pipeline (local SD/ComfyUI) and define a “concept frame” recipe
- [ ] Choose a TTS path (local first if possible); set env toggles
- [ ] Define beat tags and palette for anthology (see Strangeletters doc)

## Optional directory skeleton

- /orchestration/
  - runner.py (graph)
  - provenance.py (helpers)
- /agents/
  - story_architect/
  - visual_engineer/
  - casting_synth/
  - audio_composer/
- /artifacts/ (gitignored)
- /style/
  - palette.yaml
  - character_silhouettes.md

## Notes

- Datacore reranker can be enabled via RERANK_ENABLE=true for sharper pulls.
- Keep “explainability first”: agents must emit what they tried, even on failure.
