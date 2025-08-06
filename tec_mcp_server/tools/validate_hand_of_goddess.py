#!/usr/bin/env python3
"""
HAND OF THE GODDESS - System Status Validator
Validates all TEC MCP Server components are operational
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def check_hybrid_intelligence():
    """Check if hybrid intelligence engine is operational"""
    try:
        from tec_core.hybrid_intelligence import get_hybrid_engine
        engine = get_hybrid_engine()
        status = engine.get_system_status()
        return {
            'status': 'OPERATIONAL',
            'details': status
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e)
        }

def check_tool_orchestrator():
    """Check if tool orchestrator is operational"""
    try:
        from tec_core.tool_orchestrator import ToolOrchestrator
        orchestrator = ToolOrchestrator()
        orchestrator.initialize()
        tools = orchestrator.list_available_tools()
        return {
            'status': 'OPERATIONAL',
            'tool_count': len(tools.get('tools', {}))
        }
    except Exception as e:
        return {
            'status': 'ERROR', 
            'error': str(e)
        }

def check_axiom_engine():
    """Check if axiom engine is operational"""
    try:
        from tec_core.axiom_engine import AxiomEngine
        engine = AxiomEngine()
        result = engine.validate_content("Test content", "narrative")
        return {
            'status': 'OPERATIONAL',
            'axiom_count': len(result.get('axiom_scores', {}))
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e)
        }

def check_memory_core():
    """Check if memory core is operational"""
    try:
        from tec_core.memory_core import MemoryCore
        memory = MemoryCore()
        memory.initialize()
        status = memory.get_status()
        return {
            'status': 'OPERATIONAL',
            'database_status': status.get('status', 'unknown')
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e)
        }

def main():
    """Run complete system validation"""
    print("🏛️  HAND OF THE GODDESS - SYSTEM STATUS VALIDATION")
    print("=" * 60)
    
    checks = {
        'Hybrid Intelligence Engine': check_hybrid_intelligence(),
        'Tool Orchestrator': check_tool_orchestrator(), 
        'Axiom Engine': check_axiom_engine(),
        'Memory Core': check_memory_core()
    }
    
    all_operational = True
    
    for component, result in checks.items():
        status = result['status']
        emoji = "✅" if status == 'OPERATIONAL' else "❌"
        print(f"{emoji} {component}: {status}")
        
        if status != 'OPERATIONAL':
            all_operational = False
            print(f"   Error: {result.get('error', 'Unknown error')}")
        else:
            # Print additional details
            if 'tool_count' in result:
                print(f"   Tools Available: {result['tool_count']}")
            if 'axiom_count' in result:
                print(f"   Axioms Loaded: {result['axiom_count']}")
            if 'database_status' in result:
                print(f"   Database: {result['database_status']}")
            if 'details' in result and isinstance(result['details'], dict):
                metrics = result['details'].get('performance_metrics', {})
                if isinstance(metrics, dict):
                    print(f"   Coherence: {metrics.get('hybrid_coherence', 0.0):.3f}")
    
    print("=" * 60)
    
    if all_operational:
        print("🎯 ALL SYSTEMS OPERATIONAL - HAND OF THE GODDESS IS READY")
        print("🚀 Ready for Docker MCP Registry deployment")
    else:
        print("⚠️  SOME SYSTEMS REQUIRE ATTENTION")
        print("🔧 Check errors above and resolve before deployment")
    
    return 0 if all_operational else 1

if __name__ == '__main__':
    sys.exit(main())
