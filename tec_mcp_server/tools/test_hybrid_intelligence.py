#!/usr/bin/env python3
"""
TEC MCP Server - Hybrid Intelligence Test Tool
Test the digital-analog synthesis capabilities
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.hybrid_intelligence import process_with_hybrid_intelligence

def main():
    """CLI tool for hybrid intelligence testing"""
    if len(sys.argv) < 2:
        print("Usage: python test_hybrid_intelligence.py <input_text> [processing_type]")
        print("Processing types: creative, logical, creative_logical")
        sys.exit(1)
    
    input_text = sys.argv[1]
    processing_type = sys.argv[2] if len(sys.argv) > 2 else 'creative_logical'
    
    print(f"🧠 Testing TEC Hybrid Intelligence Engine")
    print(f"📝 Input: {input_text[:100]}{'...' if len(input_text) > 100 else ''}")
    print(f"🔄 Processing Type: {processing_type}")
    print("=" * 60)
    
    try:
        result = process_with_hybrid_intelligence(input_text, processing_type)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
