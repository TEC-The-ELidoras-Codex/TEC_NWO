#!/usr/bin/env python3
"""
TEC MCP Server - Model Context Protocol Interface
The sovereign intelligence gateway for The Elidoras Codex

This module provides the MCP protocol-compliant interface for the TEC Asimov Engine,
allowing any MCP client to access our sovereign tools and knowledge base.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

# Add the tec_core to the path
sys.path.insert(0, str(Path(__file__).parent))

from tec_core.axiom_engine import AxiomEngine
from tec_core.memory_core import MemoryCore
from tec_core.tool_orchestrator import ToolOrchestrator

# MCP imports (will need to install mcp package)
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
except ImportError:
    print("⚠️  MCP package not found. Install with: pip install mcp")
    sys.exit(1)

logger = logging.getLogger(__name__)

class TECMCPServer:
    """
    TEC Model Context Protocol Server
    
    Provides MCP-compliant access to the TEC ecosystem:
    - Axiom validation tools
    - Memory core queries
    - Lore generation
    - Asset management
    """
    
    def __init__(self):
        self.server = Server("tec-asimov-engine")
        self.axiom_engine = AxiomEngine()
        self.memory_core = MemoryCore()
        self.tool_orchestrator = ToolOrchestrator()
        
        # Register MCP tools
        self._register_tools()
        self._register_resources()
        
        logger.info("🏛️  TEC MCP Server initialized")
    
    def _register_tools(self):
        """Register all TEC tools with the MCP server"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Return available TEC tools"""
            return [
                Tool(
                    name="validate_axioms",
                    description="Validate content against the Eight Foundational Axioms of TEC",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content to validate against axioms"
                            },
                            "content_type": {
                                "type": "string", 
                                "description": "Type of content (story, decision, policy, etc.)",
                                "enum": ["story", "decision", "policy", "dialogue", "narrative", "lore", "asset"]
                            }
                        },
                        "required": ["content"]
                    }
                ),
                Tool(
                    name="query_memory",
                    description="Query the TEC Memory Core for historical context and precedents",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query for the memory core"
                            },
                            "context_type": {
                                "type": "string",
                                "description": "Type of context to search",
                                "enum": ["general", "lore", "character", "faction", "timeline", "axiom"]
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="generate_lore",
                    description="Generate TEC lore entries based on input and existing context",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creative_input": {
                                "type": "string",
                                "description": "Raw creative input to structure into lore"
                            },
                            "lore_type": {
                                "type": "string",
                                "description": "Type of lore to generate",
                                "enum": ["character", "faction", "location", "event", "technology", "philosophy"]
                            },
                            "context": {
                                "type": "object",
                                "description": "Additional context for lore generation"
                            }
                        },
                        "required": ["creative_input", "lore_type"]
                    }
                ),
                Tool(
                    name="process_asset",
                    description="Process and analyze TEC assets (audio, video, text files)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "asset_path": {
                                "type": "string",
                                "description": "Path to the asset file"
                            },
                            "asset_type": {
                                "type": "string",
                                "description": "Type of asset",
                                "enum": ["audio", "video", "text", "image", "document"]
                            },
                            "analysis_type": {
                                "type": "string",
                                "description": "Type of analysis to perform",
                                "enum": ["transcript", "summary", "entities", "concepts", "axiom_alignment"]
                            }
                        },
                        "required": ["asset_path", "asset_type"]
                    }
                ),
                Tool(
                    name="hybrid_synthesis",
                    description="Ellison-Asimov hybrid intelligence synthesis for creative-logical processing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "creative_input": {
                                "type": "string",
                                "description": "Raw, chaotic creative input (Ellison mode)"
                            },
                            "synthesis_goal": {
                                "type": "string",
                                "description": "Structured output goal (Asimov mode)",
                                "enum": ["story", "script", "lore", "policy", "analysis", "decision"]
                            },
                            "context": {
                                "type": "object",
                                "description": "Additional context for synthesis"
                            }
                        },
                        "required": ["creative_input", "synthesis_goal"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute TEC tools"""
            try:
                if name == "validate_axioms":
                    result = await self._validate_axioms(arguments)
                elif name == "query_memory":
                    result = await self._query_memory(arguments)
                elif name == "generate_lore":
                    result = await self._generate_lore(arguments)
                elif name == "process_asset":
                    result = await self._process_asset(arguments)
                elif name == "hybrid_synthesis":
                    result = await self._hybrid_synthesis(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Tool execution error: {str(e)}")
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]
    
    def _register_resources(self):
        """Register TEC resources with the MCP server"""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """Return available TEC resources"""
            return [
                Resource(
                    uri="tec://axioms",
                    name="The Eight Foundational Axioms",
                    description="The constitutional foundation of The Elidoras Codex",
                    mimeType="application/json"
                ),
                Resource(
                    uri="tec://memory/core",
                    name="TEC Memory Core",
                    description="Historical context and precedent database",
                    mimeType="application/json"
                ),
                Resource(
                    uri="tec://lore/manifest",
                    name="TEC Lore Manifest",
                    description="Complete catalog of TEC universe lore",
                    mimeType="application/json"
                ),
                Resource(
                    uri="tec://assets/manifest",
                    name="TEC Asset Manifest",
                    description="Catalog of all TEC digital assets",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read TEC resources"""
            if uri == "tec://axioms":
                return json.dumps(self.axiom_engine.get_axiom_summary(), indent=2)
            elif uri == "tec://memory/core":
                return json.dumps(self.memory_core.get_status(), indent=2)
            elif uri == "tec://lore/manifest":
                return json.dumps({"status": "lore_manifest_placeholder"}, indent=2)
            elif uri == "tec://assets/manifest":
                return json.dumps({"status": "asset_manifest_placeholder"}, indent=2)
            else:
                raise ValueError(f"Unknown resource: {uri}")
    
    # Tool implementation methods
    async def _validate_axioms(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content against axioms"""
        content = args.get("content", "")
        content_type = args.get("content_type", "general")
        
        return self.axiom_engine.validate_content(content, content_type)
    
    async def _query_memory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Query the memory core"""
        query = args.get("query", "")
        context_type = args.get("context_type", "general")
        
        results = self.memory_core.semantic_search(query, context_type)
        return {
            "results": results,
            "query": query,
            "context_type": context_type
        }
    
    async def _generate_lore(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate lore entries"""
        creative_input = args.get("creative_input", "")
        lore_type = args.get("lore_type", "general")
        context = args.get("context", {})
        
        # Use the hybrid synthesis tool for lore generation
        tool_config = {"type": "hybrid_synthesis"}
        parameters = {
            "creative_input": creative_input,
            "output_type": lore_type,
            "context": context
        }
        
        return self.tool_orchestrator._handle_hybrid_synthesis(tool_config, parameters)
    
    async def _process_asset(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Process TEC assets"""
        asset_path = args.get("asset_path", "")
        asset_type = args.get("asset_type", "text")
        analysis_type = args.get("analysis_type", "summary")
        
        # Use memory integration for asset processing
        tool_config = {"type": "memory_integration"}
        parameters = {
            "asset_path": asset_path,
            "asset_type": asset_type,
            "analysis_type": analysis_type
        }
        
        return self.tool_orchestrator._handle_memory_integration(tool_config, parameters)
    
    async def _hybrid_synthesis(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Ellison-Asimov hybrid synthesis"""
        creative_input = args.get("creative_input", "")
        synthesis_goal = args.get("synthesis_goal", "analysis")
        context = args.get("context", {})
        
        # Get memory context first
        memory_context = self.memory_core.get_relevant_context(creative_input)
        
        # Process through creative input handler
        structured_output = self.tool_orchestrator.process_creative_input(
            creative_input, memory_context, context
        )
        
        return {
            "structured_output": structured_output,
            "synthesis_goal": synthesis_goal,
            "memory_context": memory_context,
            "timestamp": datetime.now().isoformat()
        }
    
    async def initialize(self):
        """Initialize all TEC components"""
        logger.info("Initializing TEC components...")
        
        # Initialize components in order
        await asyncio.create_task(
            asyncio.to_thread(self.axiom_engine.initialize)
        )
        await asyncio.create_task(
            asyncio.to_thread(self.memory_core.initialize)
        )
        await asyncio.create_task(
            asyncio.to_thread(self.tool_orchestrator.initialize)
        )
        
        logger.info("🚀 TEC MCP Server fully operational")

async def main():
    """Main entry point for the TEC MCP Server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and initialize the TEC MCP Server
    tec_server = TECMCPServer()
    await tec_server.initialize()
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await tec_server.server.run(
            read_stream,
            write_stream,
            tec_server.server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
