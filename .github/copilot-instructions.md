# TEC (The Elidoras Codex) — Sovereign Copilot Protocol v4.0

AKA: The Sovereign Asset Protocol • The Asimov Engine Playbook • MCP Intelligence Architecture

Purpose: Embed TEC’s vision, ethics, and business model directly into our creative operating system so that any agent (human or AI) can ingest chaos and ship canon—profitably, transparently, and at scale.

---

0) Executive Summary

- Vision: A sovereign, auditable, and evolving knowledge base that turns raw streams (text/audio/video/URLs) into canon-grade lore, scripts, and assets.
- Method: Model Context Protocol (MCP) + reproducible pipelines + axiom validation + immutable versioning.
- Outcome: A studio-in-a-box capable of Love, Death & Robots–level anthology output—scripts → concept frames → voices → score—under clear rights, revenue splits, and provenance.

North Stars (Eight Foundational Axioms)

1. Narrative Supremacy – Story controls reality here; everything serves canon.
2. Duality Principle – Reject binaries; design for grey, tradeoffs, and paradox.
3. Flawed Hero Doctrine – Heroes are engines of struggle, not perfection.
4. Justifiable Force – Violence is justified only to protect innocents.
5. Sovereign Accountability – Power = service + transparency, or it’s revoked.
6. Authentic Performance – Excellence is demonstrated, not declared.
7. Transparency Mandate – Truth must be visible: logs, audits, provenance.
8. Generational Responsibility – Leave assets better than we found them.

---

1) Business Model (Money In, Money Out)

Revenue Streams

- Studio Releases (Anthology): Seasonal drops of short films / audio dramas / illustrated stories. Monetization: DTC bundles, limited collector editions, platform rev-share, licensing.
- IP Licensing: Canon packs (lore bibles, silhouettes, palettes, SFX kits) licensed to partners/game mods.
- Creator Tooling: TEC Copilot Toolkit (MCP server + agents + templates) via tiered subscription.
- Marketplace (Assets): Concept frames, score stems, VO packs, glyph fonts → revenue share 70/30 in favor of creators.
- Custom Commissions; Education (masterclass + licenses).

Rights & Splits

- Default: TEC retains canon + creator retains personal portfolio rights.
- Splits: originals 70/30 TEC/creators; marketplace 70/30 creator/platform; commissions 80/20 creator/platform.

Cost Controls

- Prefer local inference and batching; cache aggressively.
- Per-run provenance.json includes cost_estimate.
- GPU budgets by project; shut-off guards by spend cap.

KPIs

- CAC/LTV per tool tier; release NPS; time-to-canon; cost-per-minute; % assets with full provenance.

---

2) System Overview (The Asimov Engine)

Core

- MCP Server: tec-asimov-engine exposes tools: validate_axioms, query_memory, process_asset, generate_lore, hybrid_synthesis.
- MemoryCore: Semantic vector store + Postgres canon tables (characters, factions, timelines, assets, rights, releases).
- AxiomEngine: Constitutional validation (block/warn/remediate).
- ToolOrchestrator: Deterministic run graphs (idempotent, resumable) with artifact hashing.

Modes

- Flask API (app.py) – REST for CI/CD & integrations.
- MCP Mode (mcp_server.py) – Direct agent interface for Copilot/Chat clients.

Container

name: tec-asimov-engine
image: tec/asimov-engine
secrets:
  - tec.azure_openai_api_key
  - tec.elevenlabs_api_key
volumes:
  - assets:/srv/tec/assets
  - memory:/srv/tec/memory

---

3) Agent Roster (Contracts)

- Story Architect → outline/beat map/pages; must pass axiom + continuity checks.
- Visual Engineer → concept frames/boards + provenance.
- Casting Synth → voice stems + timing metadata.
- Audio Composer → stems + cue sheet.
- Coordinator → phases, artifacts, resume last green.

---

4) Asset Processing Pipeline

Ingest → Analyze → Connect → Validate → Store → Version, with provenance.json minimum fields.

---

5) Data Model (Canon Tables)

- Characters, Factions, Timelines, Assets & Rights (examples included in repo docs).

---

6) Observability & Audits

- Run log JSONL, web capture artifacts, provenance on every artifact, health status.

---

7) Security & Governance

- No Backdoors. Axiom Council PR Gate (fail 4 & 7 hard). Privacy by Design. Compliance.

---

8) Creative Doctrine (Horror & Significance)

- Laws of the Dying World; Archetype Grid; Beat Tags.

---

9) Tooling: Local-First Stack

- Text: local LLM preferred; fall back to Azure OpenAI via toggle.
- Vision/Audio: local-first; paid services gated by env.
- Search: Chroma/FAISS; reranker toggle.

---

10) Repos, Paths & Drives (Organization)

- GitHub: TEC-The-ELidoras-Codex/TEC_NWO + engine repo.
- Local Windows: C:\Users\Ghedd\TEC_CODE\TEC_NWO (synced to GitHub & Drive).
- Drive: master docs and project folders.
- Project skeleton aligned to repo structure.

---

11) Checklists

- Project Init; Run a Story; Publish (as detailed in v4 brief).

---

12) CLI & Ops

- Build & Run commands for MCP and Flask; Docker notes; health endpoints.

---

13) Templates

- Beat Map JSON and Release Manifest YAML.

---

14) Ethics & Risk; 15) Roadmap; 16) Glossary

---

Final Word: Operationalize a universe—ethically, profitably, and with receipts. Build. Validate. Commit. Ship.
