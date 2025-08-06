#!/usr/bin/env python3
"""
TEC MCP Server - Validate Axioms Tool
Constitutional content validation against Eight Foundational Axioms
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.axiom_engine import AxiomEngine

def main():
    """CLI tool for axiom validation"""
    if len(sys.argv) < 3:
        print("Usage: python validate_axioms.py <content> <content_type>")
        sys.exit(1)
    
    content = sys.argv[1]
    content_type = sys.argv[2]
    
    engine = AxiomEngine()
    result = engine.validate_content(content, content_type)
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
