# Linear MCP integration (VS Code)

This adds Linear as an MCP server in VS Code without storing secrets in the repo.

Prereqs

- Install the Model Context Protocol (MCP) extension for VS Code.
- Ensure Node.js 18+ is installed for `npx`.

Steps

1) Open the command palette and run: MCP: Add Server
2) Choose Command (stdio)
3) When prompted for the command, enter:
   `npx mcp-remote https://mcp.linear.app/sse`
4) Name it: Linear
5) Start it via MCP: List Servers → Linear → Start Server

Auth

- In VS Code, when prompted, paste your Linear API Key. Do NOT commit keys here.
- Project: TEC_HORRORIFIC_MASTERCLASS (team key TEC). URL: <https://linear.app/tec-horrorificmasterclass>

Notes

- You can now use prompts that call Linear tools (create issues, search, etc.).
- Keep keys in your OS keychain or VS Code secret storage. Never in git.
