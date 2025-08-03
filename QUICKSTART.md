# 🚀 TEC System Quick Start Guide

Welcome to The Elidoras Codex system. This guide will get you operational quickly.

## Prerequisites

- Node.js 18+ 
- npm 8+
- PostgreSQL (optional, for persistent storage)
- Azure OpenAI API access (optional, for full AI capabilities)

## Instant Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
```bash
# Copy the environment template
cp .env.template .env

# Edit .env with your configuration
# At minimum, set these for basic operation:
NODE_ENV=development
PORT=3001
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### 3. Start the System
```bash
# Development mode (with auto-restart)
npm run dev

# Or use the intelligent startup script
node start.js

# Production build and start
npm run start:prod
```

### 4. Access the Interface
- **Web Interface**: http://localhost:3001/
- **API Health Check**: http://localhost:3001/health
- **Axioms Endpoint**: http://localhost:3001/api/axioms

## Core Features Available Immediately

### 🧠 Content Analysis Engine
Test any content against the 8 Foundational Axioms:
```bash
curl -X POST http://localhost:3001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "Your content here", "type": "validate"}'
```

### ⚖️ Axiom Validation
Quick validation check:
```bash
curl -X POST http://localhost:3001/api/validate \
  -H "Content-Type: application/json" \
  -d '{"content": "Test content for axiom compliance"}'
```

### 🏛️ Historical Precedent Search
Find relevant historical patterns:
```bash
curl -X POST http://localhost:3001/api/precedents \
  -H "Content-Type: application/json" \
  -d '{"situation": "Democratic transition challenges"}'
```

### 💬 Dialogue Interface
Start collaborative human-AI sessions:
```bash
curl -X POST http://localhost:3001/api/dialogue/start \
  -H "Content-Type: application/json" \
  -d '{"userId": "user1", "topic": "Constitutional frameworks"}'
```

## System Status Commands

```bash
# Check system health
curl http://localhost:3001/health

# View system metrics
curl http://localhost:3001/api/status

# View available axioms
curl http://localhost:3001/api/axioms

# Check memory core statistics
curl http://localhost:3001/api/memory/stats
```

## Web Interface Features

The web interface at `http://localhost:3001/` provides:

- **Real-time Content Analysis** - Test content against TEC axioms
- **Interactive Dialogue System** - Collaborate with The Ellison & Asimov
- **System Monitoring** - Live status and metrics
- **Axiom Explorer** - Browse the 8 Foundational Axioms

## Development Commands

```bash
# Watch mode for development
npm run dev

# Build TypeScript
npm run build

# Run tests
npm run test

# Lint code
npm run lint

# Format code
npm run format
```

## Docker Quick Start

```bash
# Build container
npm run docker:build

# Run container
npm run docker:run
```

## Troubleshooting

### System Won't Start
1. Check environment variables: `cat .env`
2. Verify dependencies: `npm install`
3. Check ports: `lsof -i :3001` (macOS/Linux) or `netstat -ano | findstr :3001` (Windows)

### AI Features Not Working
1. Verify Azure OpenAI configuration in `.env`
2. Test API key access
3. Check endpoint format: `https://your-resource.openai.azure.com/`

### Database Connection Issues
1. System runs without database (memory-only mode)
2. For persistence, configure `DATABASE_URL` in `.env`
3. Check PostgreSQL is running: `pg_isready` (if installed)

## System Architecture

The TEC system consists of:

- **TECSystem.ts** - Main orchestration hub
- **AxiomEngine.ts** - Validates content against 8 axioms
- **AsimovService.ts** - AI logic and analysis engine  
- **MemoryCore.ts** - Historical precedent database
- **DialogueInterface.ts** - Human-AI collaboration engine
- **server.ts** - REST API and WebSocket server

## Next Steps

1. **Configure Azure OpenAI** for full AI capabilities
2. **Set up PostgreSQL** for persistent storage  
3. **Customize axioms** in `src/core/axioms/AxiomEngine.ts`
4. **Add historical events** in `src/core/memory/MemoryCore.ts`
5. **Deploy to Azure** using the included Bicep templates

## Support

The system is designed to be resilient and self-documenting. Check:

- System logs for detailed operation information
- `/health` endpoint for real-time status
- Built-in error messages and suggestions

---

**STATUS: OPERATIONAL**

*"This is not a game. This is not a drill. This is the work."* - The Architect
