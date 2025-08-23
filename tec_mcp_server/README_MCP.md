# TEC MCP SERVER - The Asimov Engine

**The Sovereign Intelligence and Central Nervous System of The Elidoras Codex**

## Overview

The TEC Asimov Engine serves as the foundational AI system for The Elidoras Codex (TEC) ecosystem. Named after Isaac Asimov, this engine embodies systematic knowledge organization and ethical AI principles while maintaining sovereign control over our digital assets and intelligence.

### Dual-Mode Architecture

The Asimov Engine operates in two complementary modes:

1. **Flask Mode (HTTP API)**: Traditional REST API for web applications and direct integrations
2. **MCP Mode (Model Context Protocol)**: Enables any MCP-compatible AI client to access TEC tools and knowledge

## Core Features

- **Axiom Validation**: All content validated against the Eight Foundational Axioms
- **Memory Core**: Semantic search and historical context retrieval
- **Hybrid Intelligence**: Ellison-Asimov synthesis (creative chaos + logical structure)
- **Asset Management**: Processing and analysis of TEC multimedia assets
- **Lore Generation**: Structured worldbuilding and narrative development

## Quick Start

### Flask Mode (Default)
```bash
# Standard web server mode
python start.py
# OR
TEC_MODE=flask python start.py
```

### MCP Mode (Model Context Protocol)
```bash
# MCP server for AI client integration
TEC_MODE=mcp python start.py
# OR directly
python mcp_server.py
```

## Docker MCP Integration

This server is designed to work with the Docker MCP ecosystem:

1. **Server Definition**: `server.yaml` in Docker MCP registry
2. **Container Support**: Dockerfile optimized for MCP protocol
3. **Volume Mapping**: Persistent storage for assets and memory
4. **Environment Variables**: Secure configuration management

### Using with Docker MCP

```yaml
# Add to your MCP client configuration
servers:
  tec-asimov-engine:
    image: tec/asimov-engine
    secrets:
      - tec.azure_openai_api_key
      - tec.elevenlabs_api_key
    parameters:
      assets: /path/to/tec/assets
      memory: /path/to/tec/memory
```

## API Endpoints (Flask Mode)

### Core Intelligence
- `GET /health` - System status and component health
- `POST /axioms/validate` - Validate content against Eight Axioms
- `POST /memory/query` - Semantic search of TEC knowledge base
- `POST /tools/execute` - Execute registered TEC tools
- `POST /synthesis/ellison-asimov` - Hybrid creative-logical processing

## MCP Tools

When running in MCP mode, the following tools are available:

- **validate_axioms**: Content validation against TEC principles
- **datacore_search**: Query the local Datacore RAG API for relevant chunks
- **query_memory**: Historical context and precedent lookup
- **generate_lore**: Structured worldbuilding and narrative creation
- **process_asset**: Analysis of multimedia TEC assets
- **hybrid_synthesis**: Ellison-Asimov creative-logical processing

## Configuration

### Environment Variables

#### Required
- `AZURE_OPENAI_API_KEY`: Azure OpenAI service key
- `ELEVENLABS_API_KEY`: ElevenLabs API key for audio processing

#### Optional
- `TEC_MODE`: Server mode (`flask` or `mcp`, default: `flask`)
- `DATACORE_URL`: The Datacore RAG endpoint for `datacore_search` (default: `http://127.0.0.1:8765/search`)
- `TEC_HOST`: Server host (default: `0.0.0.0`)
- `TEC_PORT`: Server port (default: `5000`)
- `TEC_DEBUG`: Debug mode (`true` or `false`)
- `TEC_ENVIRONMENT`: Environment mode (`development`, `staging`, `production`)
- `ENCRYPTION_KEY`: Data encryption key

### Directory Structure
```
tec_mcp_server/
├── app.py              # Flask application
├── mcp_server.py       # MCP protocol server
├── start.py            # Universal startup script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
├── .env                # Environment configuration
└── tec_core/           # Core intelligence modules
    ├── axiom_engine.py      # Axiom validation
    ├── memory_core.py       # Knowledge management
    └── tool_orchestrator.py # Tool execution
```

## The Eight Foundational Axioms

The Asimov Engine validates all content against these constitutional principles:

1. **Narrative Supremacy**: The story defines reality
2. **Duality Principle**: Truth exists in tension between opposites
3. **Flawed Hero Doctrine**: Heroes defined by struggles, not victories
4. **Justifiable Force Doctrine**: Violence only for protection/justice
5. **Sovereign Accountability**: Power earned through service
6. **Authentic Performance**: Excellence in action, not intention
7. **Transparency Mandate**: Truth must be accessible
8. **Generational Responsibility**: Consider impact on future generations

## Development

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python test_server.py
```

### Docker Build
```bash
docker build -t tec/asimov-engine .
```

## Integration Examples

### MCP Client (Python)
```python
from mcp import Client

async def query_tec():
    async with Client("tec-asimov-engine") as client:
        result = await client.call_tool("validate_axioms", {
            "content": "Our new policy proposal...",
            "content_type": "policy"
        })
        return result
```

### HTTP API (curl)
```bash
curl -X POST http://localhost:5000/axioms/validate \
  -H "Content-Type: application/json" \
  -d '{"content": "Our story begins...", "type": "narrative"}'
```

## Philosophical Foundation

> "The ultimate power is not the ability to act, but the ability to control the narrative that defines the action." - The Architect

The Asimov Engine serves as the logical counterpart to human creativity, ensuring all TEC operations align with our foundational principles while facilitating the free flow of ideas and knowledge.

---

**Genesis Version**: 080425_SOVEREIGN_001  
**Status**: OPERATIONAL  
**Protocol**: Model Context Protocol v1.0  
**Digital Cathedral**: Online
