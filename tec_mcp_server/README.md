# TEC MCP Server - The Asimov Engine

**Genesis Version: 071225_001**

The central nervous system of The Elidoras Codex (TEC) ecosystem. This MCP (Multi-Copilot Platform) server acts as the sovereign intelligence, orchestrating all TEC components while maintaining unwavering adherence to the Eight Axioms of the Architect.

## Architecture Overview

The Asimov Engine serves as the logical counterpart to human creativity, ensuring all operations align with TEC's foundational principles through three core components:

### 🏛️ Core Components

1. **Axiom Engine** (`tec_core/axiom_engine.py`)
   - Validates all content against the Eight Axioms of the Architect
   - Provides axiom-based scoring and recommendations
   - Maintains audit trail of all validations

2. **Memory Core** (`tec_core/memory_core.py`)
   - Manages PostgreSQL database connections
   - Provides semantic search across historical precedents
   - Integrates lore, memories, and contextual data

3. **Tool Orchestrator** (`tec_core/tool_orchestrator.py`)
   - Coordinates execution of specialized tools and scripts
   - Manages hybrid Ellison-Asimov synthesis
   - Handles both built-in and external tool integration

## The Eight Axioms of the Architect

1. **Narrative Supremacy** - The story defines reality; control the narrative, control the outcome
2. **Duality Principle** - All truth exists in the tension between opposites; reject binary thinking  
3. **Flawed Hero Doctrine** - True heroes are defined by their struggles, not their victories
4. **Justifiable Force Doctrine** - Violence is only moral when protecting the innocent or preserving justice
5. **Sovereign Accountability** - Power must be earned through service and maintained through transparency
6. **Authentic Performance** - Excellence in action, not just intention; authenticity over appearance
7. **Transparency Mandate** - Truth must be accessible; secrets serve only the corrupt
8. **Generational Responsibility** - Every action must consider its impact on future generations

## API Endpoints

### Health & Status
- `GET /health` - System health and component status

### Axiom Validation
- `POST /axioms/validate` - Validate content against the Eight Axioms
  ```json
  {
    "content": "Your content to validate",
    "type": "story|decision|policy|dialogue|narrative"
  }
  ```

### Memory Operations
- `POST /memory/query` - Query the TEC Memory Core
  ```json
  {
    "query": "Your search query",
    "context_type": "general|lore|precedent"
  }
  ```

### Tool Execution
- `POST /tools/execute` - Execute tools through the orchestrator
  ```json
  {
    "tool_name": "narrative_generator",
    "parameters": {"prompt": "Your prompt", "style": "balanced"}
  }
  ```

### Hybrid Intelligence
- `POST /synthesis/ellison-asimov` - Core hybrid intelligence processing
  ```json
  {
    "creative_input": "Your chaotic creative input",
    "context": {"additional": "context"}
  }
  ```

## Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your configuration
# Especially DATABASE_URL and AZURE_OPENAI_* settings
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
Ensure your PostgreSQL database is running and accessible via the `DATABASE_URL` in your `.env` file.

### 4. Run the Server
```bash
python app.py
```

The Asimov Engine will be available at `http://localhost:5000`

## Docker Deployment

### Build Container
```bash
docker build -t tec-asimov-engine .
```

### Run Container
```bash
docker run -p 5000:5000 --env-file .env tec-asimov-engine
```

## Integration with TEC Ecosystem

The Asimov Engine is designed to integrate seamlessly with:

- **TEC Main Server** (Node.js/TypeScript) - Via REST API calls
- **World Anvil API** - For lore management and world-building
- **Agentic Processor** - For advanced narrative generation
- **Azure OpenAI** - For AI-powered analysis and generation
- **PostgreSQL + Vector DB** - For persistent memory and semantic search

## Tool Development

### Adding Custom Tools

1. Create a Python script in the `tools/` directory
2. The script should accept JSON parameters via command line
3. Return results as JSON to stdout
4. The Tool Orchestrator will automatically discover and register it

Example tool structure:
```python
#!/usr/bin/env python3
import json
import sys

def main():
    # Get parameters from command line
    params = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    
    # Your tool logic here
    result = {"success": True, "output": "Tool result"}
    
    # Return JSON result
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

### Built-in Tools

The system includes these built-in tools:
- **narrative_generator** - Generate TEC-aligned narratives
- **axiom_analyzer** - Deep axiom analysis
- **ellison_asimov_synthesis** - Hybrid intelligence processing
- **memory_integrator** - Memory system integration

## Security Considerations

- All tool executions are validated through the Axiom Engine
- Non-root user execution in Docker container
- JWT-based authentication (when configured)
- Audit trail for all operations
- Input sanitization and validation

## Monitoring

The server provides comprehensive monitoring through:
- Health check endpoint (`/health`)
- Structured logging with timestamps
- Request/response timing
- Component status tracking
- Tool execution history

## Development Notes

### The Ellison-Asimov Pattern

This server embodies the core TEC philosophy of hybrid intelligence:
- **Ellison** (Human) - Chaotic, creative, intuitive input
- **Asimov** (AI) - Logical, structured, systematic processing

The `/synthesis/ellison-asimov` endpoint is where this synthesis occurs, taking raw creative input and structuring it into actionable intelligence while maintaining axiom compliance.

### Axiom-Driven Development

Every feature and tool must:
1. Pass axiom validation before execution
2. Contribute to the TEC ecosystem's coherence
3. Maintain transparency and accountability
4. Consider generational impact

---

*"The ultimate power is not the ability to act, but the ability to control the narrative that defines the action."* - The Architect

**Status**: Genesis Phase - Ready for Integration
**Next Phase**: Connect to TEC main server and begin tool orchestration
