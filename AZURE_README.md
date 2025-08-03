# Azure Configuration for The Elidoras Codex

## Overview
This directory contains all Azure deployment configurations for The Elidoras Codex platform, implementing a secure, scalable, and cost-effective cloud architecture.

## Architecture
- **Container Apps**: Main application hosting
- **Azure OpenAI**: AI reasoning engine
- **PostgreSQL Flexible Server**: Structured data storage
- **Azure AI Search**: Vector database for semantic search
- **Key Vault**: Secrets management
- **Storage Account**: File storage and static assets
- **Application Insights**: Monitoring and telemetry

## Deployment Guide

### Prerequisites
1. Azure CLI installed and configured
2. Azure subscription with sufficient permissions
3. Domain name for custom routing (optional)

### Quick Deployment
```bash
# Clone and navigate to project
git clone https://github.com/Elidorascodex/the-elidoras-codex.git
cd the-elidoras-codex

# Deploy infrastructure
az deployment group create \
  --resource-group tec-production \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json

# Deploy application
az containerapp update \
  --name tec-app \
  --resource-group tec-production \
  --image tecregistry.azurecr.io/elidoras-codex:latest
```

### Environment-Specific Deployments
- **Development**: `infra/environments/dev.parameters.json`
- **Staging**: `infra/environments/staging.parameters.json`
- **Production**: `infra/environments/prod.parameters.json`

## Configuration Files

### Infrastructure as Code
- `main.bicep`: Primary infrastructure template
- `modules/`: Reusable Bicep modules
- `environments/`: Environment-specific parameters

### Container Configuration
- `containerapp.yaml`: Container Apps configuration
- `Dockerfile`: Multi-stage container build
- `docker-compose.yml`: Local development environment

### CI/CD Pipeline
- `.github/workflows/`: GitHub Actions workflows
- `azure-pipelines.yml`: Azure DevOps pipeline

## Security Configuration

### Network Security
- Private endpoints for all data services
- Application Gateway with WAF
- Network security groups with minimal access
- Virtual network integration

### Identity and Access
- Managed Identity for service-to-service authentication
- Azure AD integration for user authentication
- Role-based access control (RBAC)
- Key Vault for secrets management

### Data Protection
- Encryption at rest and in transit
- Azure Backup for data recovery
- Point-in-time restore capabilities
- Compliance with GDPR and SOC 2

## Monitoring and Observability

### Application Insights
- Custom telemetry for axiom validation
- Performance monitoring
- Error tracking and alerting
- User behavior analytics

### Log Analytics
- Centralized logging
- Custom queries and dashboards
- Automated alerting rules
- Security event monitoring

## Cost Optimization

### Resource Sizing
- Container Apps: Optimized for workload patterns
- Database: Right-sized with auto-scaling
- Storage: Lifecycle management policies
- AI Services: Usage-based pricing monitoring

### Cost Controls
- Budget alerts and spending limits
- Resource tagging for cost allocation
- Automated scaling policies
- Reserved instance recommendations

## Disaster Recovery

### Backup Strategy
- Automated database backups
- Application configuration backups
- Code repository redundancy
- Documentation and runbook backups

### Recovery Procedures
- RTO: 4 hours for critical systems
- RPO: 1 hour for data loss tolerance
- Multi-region deployment capability
- Automated failover procedures

## Development Workflow

### Local Development
```bash
# Start local environment
docker-compose up -d

# Run with hot reload
npm run dev

# Run tests
npm test
```

### CI/CD Pipeline
1. **Build**: Compile TypeScript, run tests
2. **Security**: Vulnerability scanning, compliance checks
3. **Deploy**: Infrastructure updates, application deployment
4. **Validate**: Health checks, axiom validation
5. **Monitor**: Performance baselines, alert configuration

## Troubleshooting

### Common Issues
- Container startup failures
- Database connection issues
- Azure OpenAI rate limiting
- Certificate expiration

### Diagnostic Commands
```bash
# Check container logs
az containerapp logs show --name tec-app --resource-group tec-production

# Monitor resource health
az monitor metrics list --resource tec-app --metric-names CPUUsage,MemoryUsage

# Validate network connectivity
az network vnet list-endpoint-services --location eastus
```

## Support

### Documentation
- [Azure Container Apps Docs](https://docs.microsoft.com/azure/container-apps/)
- [Azure OpenAI Service Docs](https://docs.microsoft.com/azure/cognitive-services/openai/)
- [Infrastructure Setup Guide](./docs/infrastructure-setup.md)

### Contact
- Infrastructure Team: infra@elidorascodex.org
- On-call Support: Available for production issues
- Community Discord: #infrastructure channel

---

*This infrastructure embodies the principles of The Elidoras Codex: transparent, resilient, and designed for collaborative intelligence.*
