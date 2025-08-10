# TEC Architecture Blueprint (Operational Extraction)

This document distills the strategic blueprint into actionable implementation layers.

## Stack Selections (Locked-In)
- Core DB: PostgreSQL 15 (Flexible Server) + pgvector extension
- ORM: Prisma (schema-first constitutional data model)
- Vector Retrieval: pgvector (phase 1) – Azure AI Search retained for future hybrid augment
- Agent Framework: LangChain (incremental; mock in Airth for now)
- Microservices: Container Apps per agent (Airth first)
- Realtime: Socket.IO (pending integration after Airth live RAG)
- Frontend: Vite + React + Zustand + Chakra (scaffold next phase)
- Secrets: Key Vault + Managed Identity (migration upcoming)

## Data Model (Initial)
See `prisma/schema.prisma`. Entities: LoreEntry, LoreVersion, Embedding, AgentMemory, Relation, TaskLog.

## Airth Service (Phase 1)
- Location: `services/airth/`
- Endpoints:
  - GET `/healthz` – health probe
  - POST `/ask` – mock answer until embeddings pipeline connected
- Upcoming: similarity retrieval + answer synthesis.

## pgvector Enablement
Run once against DB:
```
psql "$DATABASE_URL" -f scripts/enable_pgvector.sql
```

## Upcoming Work (Ordered)
1. Embedding pipeline script (generate + store vectors)
2. Replace Airth mock with LangChain RAG chain
3. Frontend scaffold + Ask Airth interface
4. Key Vault secret retrieval refactor
5. ThoughtMap ingestion endpoint -> lore entries + embeddings
6. Observability: correlation IDs, structured logs

## Testing Strategy
- CI: prisma format + migrate diff validation
- Unit: Airth /healthz, expansion stubs
- Integration (later): ephemeral Postgres + vector similarity test

## Principle Mapping
| Principle | Implementation Hook |
|-----------|---------------------|
| Narrative Supremacy | Canonical version pointer in LoreEntry |
| Transparency Mandate | Prisma schema under Git + migrations |
| Generational Responsibility | Append-only LoreVersion + audit |

## Contribution Notes
Schema changes: modify -> `npm run prisma:format` -> `npm run prisma:migrate` -> commit. Avoid manual DB drift.
