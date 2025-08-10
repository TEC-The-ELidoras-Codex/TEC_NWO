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

## Decision Log (Pending)
1. Nuclear history purge: DEFERRED (needs explicit go/no-go)
2. Phase 2 priority: ThoughtMap AI expansion vs deeper MCP enrichment – NOT CHOSEN
3. Local model (Ollama) vs remote API (Azure OpenAI) – NOT CHOSEN

## Next Task Checklist
- [ ] Decide purge now vs later (record in this file under Decisions Executed)
- [ ] Implement ThoughtMap Phase 2 AI expansion (expand_node, synthesize_branch)
- [ ] Wire Ctrl+Space hotkey to expansion
- [ ] Persist save format version bump (add `schemaVersion: 2`)
- [ ] MCP adapter: export node graph to Memory Core ingestion stub
- [ ] Pre-commit large file guard (>10MB unless LFS tracked)
- [ ] Lightweight Jest smoke test for TS utils + Python self-test

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

## Suggested Order of Operations (If Continuing Immediately)
1. Commit this handoff file
2. Implement stubs (done partially in repo once committed)
3. Choose purge strategy; if YES, perform after verifying new stubs committed
4. Integrate expansion UI + persistence version bump
5. Add tests + hook install script

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
