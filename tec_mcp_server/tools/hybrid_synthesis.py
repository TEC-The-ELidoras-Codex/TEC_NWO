#!/usr/bin/env python3
"""
TEC MCP Server - Hybrid Synthesis Tool
Ellison-Asimov creative-logical processing
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.tool_orchestrator import ToolOrchestrator

def main():
    """CLI tool for hybrid synthesis"""
    if len(sys.argv) < 2:
        print("Usage: python hybrid_synthesis.py <input_text> [analysis_type]")
        sys.exit(1)
    
    input_text = sys.argv[1]
    analysis_type = sys.argv[2] if len(sys.argv) > 2 else 'creative_logical'
    
    orchestrator = ToolOrchestrator()
    orchestrator.initialize()
    
    result = orchestrator.execute_tool('ellison_asimov_synthesis', {
        'creative_input': input_text,
        'context': {'analysis_type': analysis_type},
        'output_format': 'structured'
    })
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
