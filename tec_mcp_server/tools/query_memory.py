#!/usr/bin/env python3
"""
TEC MCP Server - Query Memory Tool
Memory core semantic search and retrieval
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.memory_core import MemoryCore

def main():
    """CLI tool for memory queries"""
    if len(sys.argv) < 2:
        print("Usage: python query_memory.py <query> [limit]")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    memory = MemoryCore()
    memory.initialize()
    result = memory.semantic_search(query, 'general', limit)
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
