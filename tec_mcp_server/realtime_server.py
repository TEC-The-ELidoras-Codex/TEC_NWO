#!/usr/bin/env python3
"""
TEC MCP Server - Real-time WebSocket Enhancement
Adds WebSocket support for real-time communication with VS Code extension
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS

# Import TEC core modules
import sys
sys.path.append(str(Path(__file__).parent))

from tec_core.tool_orchestrator import ToolOrchestrator
from tec_core.memory_schemas import MemoryCoreSchema
from tec_core.hybrid_intelligence import get_hybrid_engine

logger = logging.getLogger(__name__)

class TECRealtimeServer:
    """Enhanced TEC MCP Server with WebSocket support"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'tec_sovereign_key_v1'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app)
        
        self.orchestrator = ToolOrchestrator()
        self.memory_core = MemoryCoreSchema()
        self.hybrid_engine = None
        self.connected_clients: Dict[str, Dict] = {}
        
        self.setup_routes()
        self.setup_websocket_events()
        
    def initialize(self):
        """Initialize all TEC components"""
        try:
            self.orchestrator.initialize()
            self.hybrid_engine = get_hybrid_engine()
            logger.info("✅ TEC Realtime Server initialized")
            return True
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            return False
    
    def setup_routes(self):
        """Setup Flask HTTP routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                'status': 'operational',
                'mode': 'realtime_mcp',
                'connected_clients': len(self.connected_clients),
                'hybrid_intelligence': self.hybrid_engine is not None,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/validate_axioms', methods=['POST'])
        def validate_axioms():
            try:
                data = request.get_json()
                content = data.get('content', '')
                content_type = data.get('content_type', 'narrative')
                validation_level = data.get('validation_level', 'moderate')
                
                result = self.orchestrator.validate_axioms(
                    content, content_type, validation_level
                )
                
                # Broadcast axiom validation event
                self.broadcast_event('axiom_validation', {
                    'content_preview': content[:100] + '...',
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                })
                
                return jsonify({
                    'success': True,
                    'result': result,
                    'processing_time': result.get('processing_time', 0)
                })
                
            except Exception as e:
                logger.error(f"Axiom validation error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/query_memory', methods=['POST'])
        def query_memory():
            try:
                data = request.get_json()
                query = data.get('query', '')
                limit = data.get('limit', 10)
                include_metadata = data.get('include_metadata', True)
                
                result = self.orchestrator.query_memory(
                    query, limit, include_metadata
                )
                
                # Broadcast memory query event
                self.broadcast_event('memory_query', {
                    'query': query,
                    'matches_found': len(result.get('fragments', [])),
                    'timestamp': datetime.now().isoformat()
                })
                
                return jsonify({
                    'success': True,
                    'result': result,
                    'processing_time': result.get('query_time', 0)
                })
                
            except Exception as e:
                logger.error(f"Memory query error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/process_asset', methods=['POST'])
        def process_asset():
            try:
                data = request.get_json()
                file_path = data.get('file_path', '')
                enable_hybrid = data.get('enable_hybrid_intelligence', True)
                
                result = self.orchestrator.process_asset(
                    file_path, enable_hybrid
                )
                
                # Broadcast asset processing event
                self.broadcast_event('asset_processed', {
                    'file_path': Path(file_path).name,
                    'fragments_created': result.get('fragments_created', 0),
                    'narrative_threads': result.get('narrative_threads', []),
                    'timestamp': datetime.now().isoformat()
                })
                
                return jsonify({
                    'success': True,
                    'result': result,
                    'processing_time': result.get('processing_time', 0)
                })
                
            except Exception as e:
                logger.error(f"Asset processing error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/hybrid_synthesis', methods=['POST'])
        def hybrid_synthesis():
            try:
                data = request.get_json()
                content = data.get('content', '')
                processing_type = data.get('processing_type', 'creative')
                include_metrics = data.get('include_performance_metrics', True)
                
                result = self.orchestrator.hybrid_synthesis(
                    content, processing_type, include_metrics
                )
                
                # Broadcast hybrid synthesis event
                self.broadcast_event('hybrid_synthesis', {
                    'processing_type': processing_type,
                    'coherence_score': result.get('performance_metrics', {}).get('final_coherence', 0),
                    'processing_pathway': result.get('processing_pathway', 'unknown'),
                    'timestamp': datetime.now().isoformat()
                })
                
                return jsonify({
                    'success': True,
                    'result': result,
                    'processing_time': result.get('processing_time', 0)
                })
                
            except Exception as e:
                logger.error(f"Hybrid synthesis error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/generate_lore', methods=['POST'])
        def generate_lore():
            try:
                data = request.get_json()
                prompt = data.get('prompt', '')
                lore_type = data.get('lore_type', 'fragment')
                narrative_context = data.get('narrative_context', {})
                
                result = self.orchestrator.generate_lore(
                    prompt, lore_type, narrative_context
                )
                
                # Broadcast lore generation event
                self.broadcast_event('lore_generated', {
                    'lore_type': lore_type,
                    'fragment_id': result.get('fragment_id', ''),
                    'themes': result.get('themes', []),
                    'timestamp': datetime.now().isoformat()
                })
                
                return jsonify({
                    'success': True,
                    'result': result,
                    'processing_time': result.get('processing_time', 0)
                })
                
            except Exception as e:
                logger.error(f"Lore generation error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/memory_export', methods=['GET'])
        def export_memory():
            """Export current memory core state"""
            try:
                export_data = self.memory_core.export_to_json()
                return jsonify({
                    'success': True,
                    'result': json.loads(export_data),
                    'export_time': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Memory export error: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def setup_websocket_events(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            client_id = request.sid
            self.connected_clients[client_id] = {
                'connected_at': datetime.now().isoformat(),
                'user_agent': request.headers.get('User-Agent', 'unknown')
            }
            
            logger.info(f"Client connected: {client_id}")
            
            # Send welcome message
            emit('server_message', {
                'type': 'welcome',
                'message': '🏛️ Connected to TEC Asimov Engine',
                'server_status': 'operational',
                'hybrid_intelligence': self.hybrid_engine is not None
            })
            
            # Send current system status
            emit('system_status', {
                'connected_clients': len(self.connected_clients),
                'memory_fragments': len(self.memory_core.fragments),
                'narrative_threads': len(self.memory_core.threads),
                'axioms_loaded': len(self.memory_core.axioms)
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            client_id = request.sid
            if client_id in self.connected_clients:
                del self.connected_clients[client_id]
            logger.info(f"Client disconnected: {client_id}")
        
        @self.socketio.on('request_memory_fragments')
        def handle_memory_request(data):
            """Handle request for memory fragments"""
            try:
                query = data.get('query', '')
                limit = data.get('limit', 10)
                
                if query:
                    # Perform search
                    result = self.orchestrator.query_memory(query, limit, True)
                    fragments = result.get('fragments', [])
                else:
                    # Return recent fragments
                    fragments = list(self.memory_core.fragments.values())[-limit:]
                
                emit('memory_fragments', {
                    'fragments': [f.to_dict() if hasattr(f, 'to_dict') else f for f in fragments],
                    'query': query,
                    'total_available': len(self.memory_core.fragments)
                })
                
            except Exception as e:
                emit('error', {'message': f'Memory request failed: {e}'})
        
        @self.socketio.on('request_narrative_threads')
        def handle_threads_request():
            """Handle request for narrative threads"""
            try:
                threads = [t.to_dict() if hasattr(t, 'to_dict') else t 
                          for t in self.memory_core.threads.values()]
                
                emit('narrative_threads', {
                    'threads': threads,
                    'total_count': len(threads)
                })
                
            except Exception as e:
                emit('error', {'message': f'Threads request failed: {e}'})
    
    def broadcast_event(self, event_type: str, data: Dict[str, Any]):
        """Broadcast event to all connected clients"""
        self.socketio.emit('tec_event', {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def run(self, host: str = '0.0.0.0', port: int = 8000, debug: bool = False):
        """Run the realtime server"""
        logger.info(f"🚀 Starting TEC Realtime Server on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)


def main():
    """Main entry point"""
    logging.basicConfig(level=logging.INFO)
    
    server = TECRealtimeServer()
    
    if server.initialize():
        print("🏛️  TEC REALTIME MCP SERVER")
        print("=" * 40)
        print("✅ Hybrid Intelligence: Operational")
        print("✅ Memory Core: Ready")
        print("✅ WebSocket Support: Enabled")
        print("✅ Tool Orchestrator: Initialized")
        print("=" * 40)
        print("🚀 Server starting...")
        
        server.run(debug=False)
    else:
        print("❌ Server initialization failed")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
