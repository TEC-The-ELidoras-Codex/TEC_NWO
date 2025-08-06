#!/usr/bin/env python3
"""
TEC MCP Server - Process Asset Tool
Multimedia asset analysis and integration
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.tool_orchestrator import ToolOrchestrator

def main():
    """CLI tool for asset processing"""
    if len(sys.argv) < 3:
        print("Usage: python process_asset.py <asset_path> <asset_type>")
        sys.exit(1)
    
    asset_path = sys.argv[1]
    asset_type = sys.argv[2]
    
    orchestrator = ToolOrchestrator()
    orchestrator.initialize()
    result = orchestrator.process_creative_input(asset_path, {}, {"asset_type": asset_type})
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
