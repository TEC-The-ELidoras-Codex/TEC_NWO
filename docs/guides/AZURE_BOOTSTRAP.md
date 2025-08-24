# Azure bootstrap (local-first, cloud-ready)

This guide ties the repo to Azure building blocks and templates.

- Reference templates: `external/azure/ai-app-templates`
- Goal: run locally first, then deploy minimal RAG API + static UI.

## Steps

1. Clone templates and samples

	- Run VS Code task: "Repos: Clone Microsoft docs & samples" (includes Azure AI App Templates)

1. Local RAG check

	- Run: "Env: Rebuild Python venv (3.11)"
	- Run: "TEC: Reset vectors → Ingest"
	- Run: "TEC: Serve RAG API (local)" and open `public/rag.html`

1. Pick a template to adapt

	- Browse `external/azure/ai-app-templates` and choose the closest fit (e.g., chat-rag, multi-agent)
	- Copy the template into `infrastructure/azure-app/` (do not commit secrets)

1. Deploy (placeholder)

	- Use your Azure subscription; create a resource group and App Service/Container Apps
	- Integrate later with GitHub Actions `ci-cd.yml` by wiring ACR + deployment step

Notes

- Keep MODEL_EMBED=local unless you explicitly switch to Azure OpenAI.
- Secrets go in GitHub Actions secrets or local `.env` files (gitignored).
