# TEC (The Elidoras Codex) Copilot Instructions

## Architecture Overview
TEC is a Human-AI collaboration platform implementing a "constitutional framework" with hybrid intelligence. The core philosophy centers on **The Grey** (rejection of binary thinking) and **The Axiom Engine** as the philosophical validator.

### Key Components (src/core/)
- **TECSystem.ts**: Central orchestrator - always initialize this first for any system-wide changes
- **AxiomEngine**: Validates ALL content against 8 foundational principles (Narrative Supremacy, Duality Principle, etc.)
- **AsimovService**: Azure OpenAI integration for logical analysis ("The Asimov" counterpart to human "Ellison")
- **MemoryCore**: Historical precedent database with vector search
- **DialogueInterface**: Real-time Human-AI collaboration engine

## Development Patterns

### Configuration-Driven Architecture
All services use `TECConfig` interface from `TECSystem.ts`. Environment variables follow pattern:
```typescript
azureOpenAI: {
  apiKey: process.env.AZURE_OPENAI_API_KEY,
  endpoint: process.env.AZURE_OPENAI_ENDPOINT,
  model: process.env.AZURE_OPENAI_MODEL || 'gpt-4'
}
```

### Axiom Validation Pattern
Every content-generating function must validate through AxiomEngine:
```typescript
const validation = await this.axiomEngine.validateContent(content, 'narrative');
if (!validation.isValid) {
  // Handle violations - never bypass axiom validation
}
```

### Error Handling Philosophy
Use "Anti-fragile" pattern - systems should strengthen under stress. Prefer graceful degradation over failures:
```typescript
status: 'initializing' | 'operational' | 'degraded' | 'offline'
```

## Critical Developer Workflows

### Development Server
- `npm run dev` - Uses nodemon with ts-node for hot reload
- Server runs on Express with WebSocket for real-time features
- Always check `TECSystem` initialization before testing AI features

### Axiom Validation Testing
- `npm run axiom:validate` - Custom script for axiom compliance testing
- Essential before any content-related commits
- Located in `src/scripts/validateAxioms.ts`

### Database Operations
- `npm run db:migrate` / `npm run db:seed` - PostgreSQL + Vector DB setup
- Connection string via `DATABASE_URL` environment variable
- Memory Core requires vector database for semantic search

## Azure Deployment Architecture

### Infrastructure as Code
- **Bicep templates** in `infra/main.bicep` - 395 lines defining complete Azure setup
- **Azure Container Apps** as compute platform (not App Service)
- **Azure Developer CLI** (`azd`) for deployment - never use raw Azure CLI for TEC

### Deployment Commands
```bash
azd up                    # Full provision + deploy
azd provision            # Infrastructure only
azd deploy              # Code deployment only
```

### Environment Configuration
- Uses `azure.yaml` for azd configuration
- Container target is `production` (see Dockerfile multi-stage)
- Key vault integration for secrets (Azure OpenAI keys, JWT secrets)

## TEC-Specific Conventions

### Content Types
All content processing uses standardized types:
```typescript
'story' | 'decision' | 'policy' | 'dialogue' | 'narrative'
```

### AI Analysis Pattern
AsimovService expects structured requests:
```typescript
analysisType: 'axiom' | 'historical' | 'narrative' | 'decision' | 'precedent'
```

### Security Philosophy
- "Privacy by design" - encrypt sensitive data
- Multi-layered security with JWT + encryption keys
- Helmet.js with CSP for Express security

## Integration Points

### Azure OpenAI Integration
- Model selection via environment (default: gpt-4)
- Analysis types map to different prompt strategies
- Always include confidence scores and reasoning chains

### Database Integration
- PostgreSQL for structured data
- Vector database for semantic search in MemoryCore
- Historical precedent patterns require vector similarity matching

### Real-time Features
- WebSocket server alongside Express
- DialogueInterface manages Human-AI conversation state
- TECSystem orchestrates real-time validation

## File Structure Importance
- `/src/core/` - Never modify without understanding TECSystem dependencies
- `/infra/` - Azure Bicep templates with resource naming conventions using `resourceToken`
- `/src/scripts/` - Custom validation and database tools

## Testing Philosophy
Focus on axiom compliance and hybrid intelligence validation rather than unit testing individual functions. The system's correctness is measured by philosophical alignment, not just technical functionality.
