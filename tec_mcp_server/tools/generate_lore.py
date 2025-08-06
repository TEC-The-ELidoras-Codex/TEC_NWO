#!/usr/bin/env python3
"""
TEC MCP Server - Generate Lore Tool
Structured worldbuilding and narrative development
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.tool_orchestrator import ToolOrchestrator

def main():
    """CLI tool for lore generation"""
    if len(sys.argv) < 2:
        print("Usage: python generate_lore.py <input_text> [lore_type]")
        sys.exit(1)
    
    input_text = sys.argv[1]
    lore_type = sys.argv[2] if len(sys.argv) > 2 else 'narrative'
    
    orchestrator = ToolOrchestrator()
    orchestrator.initialize()
    
    result = orchestrator.execute_tool('narrative_generation', {
        'input_text': input_text,
        'lore_type': lore_type,
        'format': 'json'
    })
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
