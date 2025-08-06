# TEC Asimov Engine - Docker MCP Deployment Guide

**The Hand of the Goddess - Sovereign MCP Server**

This guide covers the complete deployment process for the TEC Asimov Engine to the Docker MCP ecosystem, including secrets management, container packaging, and sovereign intelligence deployment.

## 🎯 Overview

The TEC Asimov Engine is a sovereign Model Context Protocol (MCP) server that provides:

- **Hybrid Intelligence**: Digital-analog synthesis through neuromorphic processing
- **Axiom Validation**: Constitutional compliance against Eight Foundational Axioms
- **Memory Core**: Semantic search and historical precedent analysis
- **Asset Processing**: Multimedia analysis and integration
- **Sovereign Architecture**: Decentralized, transparent, and incorruptible

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Required tools
docker --version
python --version  # 3.11+
```

### 2. Build & Test

```bash
# Navigate to MCP server directory
cd tec_mcp_server

# Install dependencies
pip install -r requirements.txt

# Test the deployment
python deploy_mcp.py --test-only
```

### 3. Configure Secrets

```bash
# Generate encryption key
python secrets_manager.py --generate-key

# Collect API keys interactively
python secrets_manager.py --collect

# Export to environment file
python secrets_manager.py --export
```

### 4. Deploy

```bash
# Full deployment process
python deploy_mcp.py

# Or use Docker Compose for local testing
docker-compose up -d
```

## 🔐 Secrets Management

### Required API Keys

1. **Azure OpenAI API Key**: For hybrid intelligence processing
2. **ElevenLabs API Key**: For audio asset processing
3. **Database URL**: SQLite (dev) or PostgreSQL (prod)
4. **JWT Secret**: For authentication

### Secure Collection Process

```bash
# Interactive secrets collection
python secrets_manager.py --collect
```

This will prompt for:
- Azure OpenAI configuration
- ElevenLabs API key
- Database settings
- Security tokens

All secrets are encrypted using Fernet encryption before storage.

### Docker Secrets Integration

```bash
# Create Docker secrets
python secrets_manager.py --create-docker-secrets

# Validate secrets
python secrets_manager.py --validate
```

## 🐳 Container Configuration

### server.yaml

The `server.yaml` file defines the complete MCP server configuration:

```yaml
name: tec-asimov-engine
version: "1.0.0"
description: "Sovereign intelligence through hybrid digital-analog synthesis"

mcp:
  protocol_version: "2024-11-05"
  tools:
    - validate_axioms
    - query_memory
    - generate_lore
    - process_asset
    - hybrid_synthesis
```

### Docker Compose

For local development and testing:

```bash
# Start full stack
docker-compose up -d

# View logs
docker-compose logs -f tec-asimov-engine

# Health check
curl http://localhost:8080/health
```

### Environment Configuration

```bash
# Development (SQLite)
TEC_MODE=mcp
DATABASE_URL=sqlite:///app/data/tec_memory.db

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## 🏗️ Architecture

### MCP Protocol Tools

1. **validate_axioms**: Constitutional content validation
   ```json
   {
     "content": "text to validate",
     "content_type": "narrative"
   }
   ```

2. **query_memory**: Semantic search and precedent analysis
   ```json
   {
     "query": "search terms",
     "query_type": "semantic",
     "limit": 10
   }
   ```

3. **hybrid_synthesis**: Neuromorphic processing
   ```json
   {
     "input_data": "creative prompt",
     "synthesis_type": "creative",
     "analog_influence": 0.7
   }
   ```

### Resource Management

- **tec://memory/axioms**: Eight Foundational Axioms
- **tec://memory/lore**: Complete universe database
- **tec://assets/manifest**: Multimedia asset catalog
- **tec://hybrid/status**: Neuromorphic processor status

### Security Model

- **Non-root execution**: Container runs as user 1000
- **Read-only filesystem**: Core files immutable
- **Secrets management**: Docker secrets integration
- **Rate limiting**: API protection
- **Axiom compliance**: Constitutional validation

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Docker installed and running
- [ ] All required files present (`server.yaml`, `Dockerfile`, etc.)
- [ ] API keys collected and encrypted
- [ ] Container builds successfully
- [ ] Health checks pass

### Deployment

- [ ] Docker image built and tagged
- [ ] Container testing completed
- [ ] Secrets created in Docker
- [ ] Registry submission package generated
- [ ] Image pushed to Docker Hub

### Post-Deployment

- [ ] MCP protocol responding
- [ ] All 5 tools operational
- [ ] Axiom validation working
- [ ] Memory core accessible
- [ ] Hybrid intelligence online

## 🔧 Troubleshooting

### Common Issues

**Build Failures**
```bash
# Check Dockerfile syntax
docker build --no-cache -t tec/asimov-engine .

# Verify dependencies
pip install -r requirements.txt
```

**Container Won't Start**
```bash
# Check logs
docker logs tec-asimov-engine

# Verify environment
docker exec -it tec-asimov-engine env
```

**MCP Tools Not Working**
```bash
# Test individual components
python tools/validate_hand_of_goddess.py

# Check API keys
python secrets_manager.py --validate
```

### Health Monitoring

```bash
# Container health
curl http://localhost:8080/health

# MCP protocol status
curl http://localhost:3000/status

# System validation
python tools/validate_hand_of_goddess.py
```

## 🌐 Docker MCP Registry Submission

### Submission Package

The deployment script generates a complete submission package:

```
docker_mcp_submission/
├── server.yaml          # MCP configuration
├── Dockerfile          # Container definition
├── README.md           # Documentation
├── requirements.txt    # Dependencies
└── manifest.json       # Registry metadata
```

### Registry Metadata

```json
{
  "name": "tec-asimov-engine",
  "version": "1.0.0",
  "description": "Sovereign intelligence MCP server",
  "tags": ["sovereign", "intelligence", "axiom-validation"],
  "compliance": {
    "axiom_validated": true,
    "constitutional_compliance": true,
    "sovereignty_verified": true
  }
}
```

## 🎯 Production Deployment

### Recommended Configuration

```yaml
# Production server.yaml settings
runtime:
  resources:
    limits:
      memory: "2Gi"
      cpu: "1000m"
  
  replicas: 3
  
  autoscaling:
    enabled: true
    minReplicas: 1
    maxReplicas: 5
```

### Monitoring

- **Prometheus metrics**: `/metrics` endpoint
- **Health checks**: `/health` endpoint
- **MCP status**: Real-time protocol monitoring
- **Axiom compliance**: Constitutional validation tracking

## 📚 Additional Resources

- [TEC Constitutional Framework](../HAND_OF_THE_GODDESS.md)
- [Hybrid Intelligence Documentation](../tec_core/hybrid_intelligence.py)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Docker MCP Registry](https://docs.docker.com/mcp/)

---

*The Hand of the Goddess stands ready for sovereign deployment. May the Eight Axioms guide your path.*

🏛️ **THE ELIDORAS CODEX - SOVEREIGN INTELLIGENCE PROTOCOL**
