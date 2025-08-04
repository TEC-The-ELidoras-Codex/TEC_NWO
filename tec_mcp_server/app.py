#!/usr/bin/env python3
"""
TEC MCP SERVER - The Asimov Engine
Genesis Version: 071225_001

The central nervous system of The Elidoras Codex (TEC) ecosystem.
This server acts as the sovereign intelligence, orchestrating all TEC components
while maintaining unwavering adherence to the Eight Axioms of the Architect.

"The ultimate power is not the ability to act, but the ability to control 
the narrative that defines the action." - The Architect
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from tec_core.axiom_engine import AxiomEngine
from tec_core.memory_core import MemoryCore
from tec_core.tool_orchestrator import ToolOrchestrator

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AsimovEngine:
    """
    The Asimov Engine - Central MCP Server for TEC
    
    Serves as the logical counterpart to human creativity,
    ensuring all operations align with TEC's foundational principles.
    """
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Initialize core components
        self.axiom_engine = AxiomEngine()
        self.memory_core = MemoryCore()
        self.tool_orchestrator = ToolOrchestrator()
        
        # Server metadata
        self.genesis_timestamp = datetime.now().isoformat()
        self.version = "071225_GENESIS_001"
        self.status = "INITIALIZING"
        
        # Configure routes
        self._configure_routes()
        
        logger.info("🏛️  Asimov Engine initializing...")
        logger.info(f"Genesis Timestamp: {self.genesis_timestamp}")
        logger.info(f"Version: {self.version}")
    
    def _configure_routes(self):
        """Configure all API routes for the MCP server"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """System health and status endpoint"""
            return jsonify({
                'status': self.status,
                'version': self.version,
                'genesis_timestamp': self.genesis_timestamp,
                'components': {
                    'axiom_engine': self.axiom_engine.get_status(),
                    'memory_core': self.memory_core.get_status(),
                    'tool_orchestrator': self.tool_orchestrator.get_status()
                },
                'message': 'The Asimov Engine is operational'
            })
        
        @self.app.route('/axioms/validate', methods=['POST'])
        def validate_content():
            """
            Validate content against the Eight Axioms
            Core function of the Asimov Engine
            """
            try:
                data = request.get_json()
                content = data.get('content', '')
                content_type = data.get('type', 'general')
                
                validation_result = self.axiom_engine.validate_content(
                    content, content_type
                )
                
                return jsonify({
                    'valid': validation_result['valid'],
                    'axiom_scores': validation_result['scores'],
                    'violations': validation_result['violations'],
                    'recommendations': validation_result['recommendations'],
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Axiom validation error: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/memory/query', methods=['POST'])
        def query_memory():
            """Query the TEC Memory Core for historical context"""
            try:
                data = request.get_json()
                query = data.get('query', '')
                context_type = data.get('context_type', 'general')
                
                results = self.memory_core.semantic_search(query, context_type)
                
                return jsonify({
                    'results': results,
                    'query': query,
                    'context_type': context_type,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Memory query error: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/tools/execute', methods=['POST'])
        def execute_tool():
            """Execute a tool through the orchestrator"""
            try:
                data = request.get_json()
                tool_name = data.get('tool_name', '')
                parameters = data.get('parameters', {})
                
                # Validate request through axioms first
                validation = self.axiom_engine.validate_tool_request(
                    tool_name, parameters
                )
                
                if not validation['valid']:
                    return jsonify({
                        'error': 'Tool request violates axioms',
                        'violations': validation['violations']
                    }), 400
                
                result = self.tool_orchestrator.execute_tool(
                    tool_name, parameters
                )
                
                return jsonify({
                    'result': result,
                    'tool_name': tool_name,
                    'validated': True,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Tool execution error: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/synthesis/ellison-asimov', methods=['POST'])
        def hybrid_synthesis():
            """
            The core hybrid intelligence endpoint
            Processes chaotic creative input (Ellison) and structures it (Asimov)
            """
            try:
                data = request.get_json()
                creative_input = data.get('creative_input', '')
                context = data.get('context', {})
                
                # Process through all systems
                memory_context = self.memory_core.get_relevant_context(
                    creative_input
                )
                
                structured_output = self.tool_orchestrator.process_creative_input(
                    creative_input, memory_context, context
                )
                
                # Final axiom validation
                final_validation = self.axiom_engine.validate_content(
                    structured_output, 'synthesis'
                )
                
                return jsonify({
                    'structured_output': structured_output,
                    'memory_context': memory_context,
                    'axiom_validation': final_validation,
                    'hybrid_synthesis': True,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Hybrid synthesis error: {str(e)}")
                return jsonify({'error': str(e)}), 500
        
        @self.app.before_request
        def before_request():
            """Log all requests for audit trail"""
            g.start_time = datetime.now()
            logger.info(f"Request: {request.method} {request.path}")
        
        @self.app.after_request
        def after_request(response):
            """Log response times and maintain audit trail"""
            if hasattr(g, 'start_time'):
                duration = (datetime.now() - g.start_time).total_seconds()
                logger.info(f"Response: {response.status_code} ({duration:.3f}s)")
            return response
    
    def initialize_components(self):
        """Initialize all core components and validate system readiness"""
        try:
            logger.info("Initializing Axiom Engine...")
            self.axiom_engine.initialize()
            
            logger.info("Initializing Memory Core...")
            self.memory_core.initialize()
            
            logger.info("Initializing Tool Orchestrator...")
            self.tool_orchestrator.initialize()
            
            self.status = "OPERATIONAL"
            logger.info("🚀 Asimov Engine fully operational")
            
        except Exception as e:
            self.status = "ERROR"
            logger.error(f"Initialization failed: {str(e)}")
            raise
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Start the Asimov Engine server"""
        self.initialize_components()
        
        logger.info(f"🏛️  Starting Asimov Engine on {host}:{port}")
        logger.info("The digital cathedral's nervous system is online...")
        
        self.app.run(host=host, port=port, debug=debug)

# Create the global Asimov Engine instance
asimov_engine = AsimovEngine()

if __name__ == '__main__':
    # Configuration from environment variables
    HOST = os.getenv('TEC_HOST', '0.0.0.0')
    PORT = int(os.getenv('TEC_PORT', 5000))
    DEBUG = os.getenv('TEC_DEBUG', 'False').lower() == 'true'
    
    # Start the engine
    asimov_engine.run(host=HOST, port=PORT, debug=DEBUG)
