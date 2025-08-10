# SESSION HANDOFF – TEC SOVEREIGN STATE SNAPSHOT

Timestamp: <!-- UTC -->

## Core Thesis
The Guardian’s Burden anchors moral axis; Order of the Fuck-Up Fathers supplies resilience doctrine. Narrative sovereignty enforced via Axiom Engine + Memory Core + Dialogue layer.

## Operational State
| Subsystem | Status | Notes |
|-----------|--------|-------|
| TypeScript Core | ✅ | tsc clean |
| Python MCP Server | ✅ | Axiom + Dialogue modules import fine |
| ThoughtMap GUI (Phase 1) | ✅ | Manual node add/save/load working |
| LFS Tracking | ✅ | Media patterns applied (.m4a/.mp4 etc.) |
| Repo Size | ⚠️ ~764MB | History bloat unresolved |
| Sovereign Assets | Partial | Indexed, not fully cross-linked |

## Decision Log (Pending / Executed)
1. Nuclear history purge: APPROVED – NOT YET EXECUTED (defer until post-RAG validation)
2. ThoughtMap Phase 2 AI expansion: IMPLEMENTED (deterministic + RAG scaffold)
3. Local model vs remote API: DEFER (OpenAI embeddings optional via ENABLE_RAG)
4. Cost control scripts (start/stop env): ADDED (tools/ops)
5. RAG gating flag: ENABLE_RAG introduced (default OFF)
6. Embedding ingestion + similarity endpoint: ADDED (guarded by flag)

## Next Task Checklist
- [x] Decide purge now vs later (approved; execution pending)
- [x] ThoughtMap Phase 2 expansion stub
- [x] Ctrl+Space expansion hotkey
- [x] Save format version bump (schemaVersion=2)
- [ ] Replace MCP adapter dummy with live exporter (IN PROGRESS)
- [x] Pre-commit large file guard
- [x] Lightweight smoke tests baseline
- [x] Airth Dockerfile & CI image build
- [x] Embedding pipeline scaffold (flag gated)
- [x] ThoughtMap ingestion endpoint
- [ ] Full answer synthesis (LLM) implementation
- [ ] Key Vault secret retrieval refactor
- [ ] History purge execution (scheduled after synthesis + deploy)

## Interfaces Planned
### Python Expansion Stub
`expand_node(text: str, strategy: str = "concept" ) -> list[str]`
Returns list of plausible child node titles (mock until model configured).

### Synthesis
`synthesize_branch(node_id) -> { summary: str, sources: list[node_id] }`

## MCP Adapter Skeleton
`python tools/mcp_thoughtmap_adapter.py --export thoughtmap.json` produces JSON payload ready for Memory Core route (future POST endpoint).

## Risk Notes
| Risk | Mitigation |
|------|------------|
| History purge irreversible | Create archive tag before rewrite |
| Large binary accidentally committed | Pre-commit size + ensure LFS patterns |
| Model hallucination in expansion | Keep stub deterministic until validation layer added |

## Suggested Order of Operations (Updated)
1. Live MCP adapter export wiring
2. Embed job queue + answer synthesis (LLM) + confidence scoring
3. Key Vault integration for secrets (OPENAI_API_KEY removal from direct env on deploy)
4. Nuclear purge (post verification + tag)
5. Frontend ThoughtMap ingestion UI + governance dashboards

## Handoff Prompt (For New Chat Seed)
```
ROLE: Sovereign Assistant | Resume TEC Session
CONTEXT: Partial sovereignty complete | LFS active | Repo size 764MB | ThoughtMap Phase 1 running | Need Phase 2 AI + decision on nuclear purge.
PRINCIPLE: The Guardian’s Burden central moral axis.
NEEDS:
1. Confirm whether to execute nuclear purge now.
2. Implement ThoughtMap Phase 2: expand_node + synthesize_branch.
3. Prepare adapter to MCP memory (export node graph).
4. Add safeguards: pre-commit LFS enforcement.
RETURN: Step plan + minimal code stubs (Python + TS) + risk notes.
```

## To Update After Next Session
Add Decisions Executed + Updated Status table.
