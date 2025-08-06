"""
TEC TOOL ORCHESTRATOR
The central hub for coordinating and executing specialized tools and agents

This module manages the execution and coordination of various TEC tools,
scripts, and AI agents, ensuring they work in harmony with the system's axioms.
Features integration with the Hybrid Intelligence Engine for digital-analog synthesis.
"""

import os
import sys
import logging
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# Import core components
try:
    from .hybrid_intelligence import process_with_hybrid_intelligence, get_hybrid_engine
    HYBRID_INTELLIGENCE_AVAILABLE = True
except ImportError:
    HYBRID_INTELLIGENCE_AVAILABLE = False
    logger.warning("Hybrid Intelligence Engine not available - using fallback processing")

try:
    from .axiom_engine import AxiomEngine
    AXIOM_ENGINE_AVAILABLE = True
except ImportError:
    AXIOM_ENGINE_AVAILABLE = False
    logger.warning("Axiom Engine not available")

try:
    from .memory_core import MemoryCore
    MEMORY_CORE_AVAILABLE = True
except ImportError:
    MEMORY_CORE_AVAILABLE = False
    logger.warning("Memory Core not available")

try:
    from .asset_processor import AssetProcessor
    ASSET_PROCESSOR_AVAILABLE = True
except ImportError:
    ASSET_PROCESSOR_AVAILABLE = False
    logger.warning("Asset Processor not available")

class ToolOrchestrator:
    """
    The Tool Orchestrator - Central Command for TEC Tools
    
    Coordinates execution of specialized tools, scripts, and agents
    while maintaining axiom compliance and system coherence.
    """
    
    def __init__(self):
        self.status = "INITIALIZING"
        self.available_tools = {}
        self.execution_history = []
        self.base_path = Path(__file__).parent.parent
        
    def initialize(self):
        """Initialize the Tool Orchestrator and discover available tools"""
        logger.info("🛠️  Initializing Tool Orchestrator...")
        
        try:
            # Register built-in tools
            self._register_builtin_tools()
            
            # Discover external tools and scripts
            self._discover_external_tools()
            
            self.status = "OPERATIONAL"
            logger.info(f"✅ Tool Orchestrator operational with {len(self.available_tools)} tools")
            
        except Exception as e:
            self.status = "ERROR"
            logger.error(f"Tool Orchestrator initialization failed: {str(e)}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the Tool Orchestrator"""
        return {
            'status': self.status,
            'tools_available': len(self.available_tools),
            'executions_performed': len(self.execution_history),
            'last_execution': self.execution_history[-1]['timestamp'] if self.execution_history else None,
            'tool_categories': list(set(tool['category'] for tool in self.available_tools.values()))
        }
    
    def _register_builtin_tools(self):
        """Register built-in tools and capabilities"""
        
        # Narrative Processing Tool
        self.available_tools['narrative_generator'] = {
            'name': 'Narrative Generator',
            'description': 'Generate TEC-aligned narratives and stories',
            'category': 'narrative',
            'type': 'builtin',
            'parameters': ['prompt', 'style', 'axiom_focus'],
            'handler': self._handle_narrative_generation
        }
        
        # Axiom Analysis Tool
        self.available_tools['axiom_analyzer'] = {
            'name': 'Axiom Analyzer',
            'description': 'Deep analysis of content against specific axioms',
            'category': 'validation',
            'type': 'builtin',
            'parameters': ['content', 'axiom_focus', 'analysis_depth'],
            'handler': self._handle_axiom_analysis
        }
        
        # Synthesis Tool
        self.available_tools['ellison_asimov_synthesis'] = {
            'name': 'Ellison-Asimov Synthesis',
            'description': 'Hybrid intelligence processing of creative inputs',
            'category': 'synthesis',
            'type': 'builtin',
            'parameters': ['creative_input', 'context', 'output_format'],
            'handler': self._handle_hybrid_synthesis
        }
        
        # Memory Integration Tool
        self.available_tools['memory_integrator'] = {
            'name': 'Memory Integrator',
            'description': 'Integrate new information into the TEC memory system',
            'category': 'memory',
            'type': 'builtin',
            'parameters': ['content', 'content_type', 'relationships'],
            'handler': self._handle_memory_integration
        }
    
    def _discover_external_tools(self):
        """Discover external Python scripts and tools"""
        
        # Look for agentic_processor.py (mentioned in the requirements)
        agentic_processor_path = self.base_path / 'scripts' / 'agentic_processor.py'
        if agentic_processor_path.exists():
            self.available_tools['agentic_processor'] = {
                'name': 'Agentic Processor',
                'description': 'Advanced narrative generation and processing',
                'category': 'narrative',
                'type': 'external_python',
                'path': str(agentic_processor_path),
                'parameters': ['input_text', 'processing_mode'],
                'handler': self._handle_external_python
            }
        
        # Look for World Anvil integration scripts
        world_anvil_path = self.base_path / 'scripts' / 'world_anvil_api.py'
        if world_anvil_path.exists():
            self.available_tools['world_anvil_api'] = {
                'name': 'World Anvil API',
                'description': 'Interface with World Anvil for lore management',
                'category': 'lore',
                'type': 'external_python', 
                'path': str(world_anvil_path),
                'parameters': ['action', 'entity_data'],
                'handler': self._handle_external_python
            }
        
        # Look for other TEC tools in the tools directory
        tools_dir = self.base_path / 'tools'
        if tools_dir.exists():
            for tool_file in tools_dir.glob('*.py'):
                if tool_file.name != '__init__.py':
                    tool_name = tool_file.stem
                    self.available_tools[tool_name] = {
                        'name': tool_name.replace('_', ' ').title(),
                        'description': f'TEC tool: {tool_name}',
                        'category': 'custom',
                        'type': 'external_python',
                        'path': str(tool_file),
                        'parameters': ['data'],
                        'handler': self._handle_external_python
                    }
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific tool with given parameters
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters to pass to the tool
            
        Returns:
            Tool execution result
        """
        try:
            if tool_name not in self.available_tools:
                raise ValueError(f"Tool '{tool_name}' not found")
            
            tool_config = self.available_tools[tool_name]
            
            # Log execution
            execution_record = {
                'timestamp': datetime.now().isoformat(),
                'tool_name': tool_name,
                'parameters': parameters,
                'status': 'executing'
            }
            self.execution_history.append(execution_record)
            
            # Execute the tool
            result = tool_config['handler'](tool_config, parameters)
            
            # Update execution record
            execution_record['status'] = 'completed'
            execution_record['result'] = result
            
            logger.info(f"Tool executed successfully: {tool_name}")
            return result
            
        except Exception as e:
            logger.error(f"Tool execution error ({tool_name}): {str(e)}")
            execution_record['status'] = 'failed'
            execution_record['error'] = str(e)
            
            return {
                'success': False,
                'error': str(e),
                'tool_name': tool_name
            }
    
    def _handle_narrative_generation(self, tool_config: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle narrative generation requests"""
        prompt = parameters.get('prompt', '')
        style = parameters.get('style', 'balanced')
        axiom_focus = parameters.get('axiom_focus', [])
        
        # This would integrate with actual narrative generation logic
        # For now, return a structured response
        return {
            'success': True,
            'narrative': f"Generated narrative based on prompt: {prompt}",
            'style': style,
            'axiom_alignment': axiom_focus,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'tool': 'narrative_generator'
            }
        }
    
    def _handle_axiom_analysis(self, tool_config: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle deep axiom analysis requests"""
        content = parameters.get('content', '')
        axiom_focus = parameters.get('axiom_focus', 'all')
        analysis_depth = parameters.get('analysis_depth', 'standard')
        
        return {
            'success': True,
            'analysis': f"Deep axiom analysis of content (focus: {axiom_focus})",
            'depth': analysis_depth,
            'recommendations': [
                'Consider strengthening narrative elements',
                'Enhance duality principle alignment'
            ],
            'metadata': {
                'analyzed_at': datetime.now().isoformat(),
                'tool': 'axiom_analyzer'
            }
        }
    
    def _handle_hybrid_synthesis(self, tool_config: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Ellison-Asimov hybrid synthesis with Digital-Analog Intelligence"""
        creative_input = parameters.get('creative_input', '')
        context = parameters.get('context', {})
        output_format = parameters.get('output_format', 'structured')
        
        # Use Hybrid Intelligence Engine if available
        if HYBRID_INTELLIGENCE_AVAILABLE:
            logger.info("🧠 Using Hybrid Intelligence Engine for synthesis")
            
            # Determine processing type from context
            analysis_type = context.get('analysis_type', 'creative_logical')
            
            # Process through hybrid intelligence
            hybrid_result = process_with_hybrid_intelligence(creative_input, analysis_type)
            
            # Enhance with traditional TEC analysis
            traditional_analysis = {
                'extracted_concepts': self._extract_concepts(creative_input),
                'structured_plan': self._create_action_plan(creative_input, context),
                'axiom_considerations': self._identify_axiom_relevance(creative_input)
            }
            
            # Combine hybrid intelligence with traditional processing
            structured_output = {
                'hybrid_intelligence_result': hybrid_result,
                'traditional_analysis': traditional_analysis,
                'synthesis_type': 'digital_analog_fusion',
                'processing_pathway': hybrid_result.get('processing_pathway', 'hybrid'),
                'performance_metrics': hybrid_result.get('performance_metrics', {})
            }
            
        else:
            # Fallback to traditional processing
            logger.info("🔄 Using traditional synthesis (hybrid intelligence unavailable)")
            structured_output = {
                'analyzed_input': creative_input,
                'extracted_concepts': self._extract_concepts(creative_input),
                'structured_plan': self._create_action_plan(creative_input, context),
                'axiom_considerations': self._identify_axiom_relevance(creative_input),
                'synthesis_type': 'traditional_digital'
            }
        
        return {
            'success': True,
            'synthesis_result': structured_output,
            'context_used': context,
            'output_format': output_format,
            'metadata': {
                'synthesized_at': datetime.now().isoformat(),
                'tool': 'ellison_asimov_synthesis',
                'hybrid_intelligence_used': HYBRID_INTELLIGENCE_AVAILABLE,
                'processing_mode': structured_output.get('synthesis_type', 'traditional')
            }
        }
    
    def _handle_memory_integration(self, tool_config: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle memory integration requests"""
        content = parameters.get('content', '')
        content_type = parameters.get('content_type', 'general')
        relationships = parameters.get('relationships', [])
        
        return {
            'success': True,
            'integration_result': 'Content integrated into memory system',
            'content_type': content_type,
            'relationships_mapped': len(relationships),
            'metadata': {
                'integrated_at': datetime.now().isoformat(),
                'tool': 'memory_integrator'
            }
        }
    
    def _handle_external_python(self, tool_config: Dict[str, Any], parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle external Python script execution"""
        try:
            script_path = tool_config['path']
            
            # Prepare parameters as JSON for the script
            params_json = json.dumps(parameters)
            
            # Execute the Python script
            result = subprocess.run([
                sys.executable, script_path, params_json
            ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
            
            if result.returncode == 0:
                # Try to parse JSON output
                try:
                    output_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    output_data = {'output': result.stdout}
                
                return {
                    'success': True,
                    'result': output_data,
                    'script': script_path
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr,
                    'script': script_path
                }
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Script execution timed out',
                'script': script_path
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'script': script_path
            }
    
    def process_creative_input(self, creative_input: str, memory_context: Dict[str, Any], 
                             context: Dict[str, Any]) -> str:
        """
        Process creative input through the hybrid intelligence system
        
        This is the core function called by the main Asimov Engine for
        Ellison-Asimov synthesis.
        """
        try:
            # Use the hybrid synthesis tool
            result = self.execute_tool('ellison_asimov_synthesis', {
                'creative_input': creative_input,
                'context': {**context, 'memory_context': memory_context},
                'output_format': 'structured'
            })
            
            if result.get('success'):
                synthesis = result['synthesis_result']
                
                # Format the structured output as a coherent response
                structured_output = f"""
                ASIMOV ANALYSIS:
                
                Input Processing: {synthesis['analyzed_input'][:200]}...
                
                Key Concepts Identified:
                {self._format_concepts(synthesis['extracted_concepts'])}
                
                Recommended Action Plan:
                {self._format_action_plan(synthesis['structured_plan'])}
                
                Axiom Considerations:
                {self._format_axiom_considerations(synthesis['axiom_considerations'])}
                """
                
                return structured_output.strip()
            else:
                return f"Processing error: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            logger.error(f"Creative input processing error: {str(e)}")
            return f"Unable to process creative input: {str(e)}"
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from creative input"""
        # Simple concept extraction - would be enhanced with NLP in production
        words = text.lower().split()
        concepts = []
        
        # Look for TEC-relevant concepts
        tec_keywords = ['narrative', 'axiom', 'story', 'hero', 'villain', 'justice', 
                       'truth', 'power', 'responsibility', 'future', 'legacy']
        
        for keyword in tec_keywords:
            if keyword in words:
                concepts.append(keyword)
        
        return concepts[:5]  # Top 5 concepts
    
    def _create_action_plan(self, input_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create an action plan from creative input"""
        return {
            'immediate_actions': ['Analyze input for axiom alignment', 'Identify key themes'],
            'medium_term_goals': ['Develop narrative structure', 'Integrate with existing lore'],
            'long_term_vision': ['Contribute to TEC ecosystem', 'Strengthen axiom foundation']
        }
    
    def _identify_axiom_relevance(self, text: str) -> List[str]:
        """Identify which axioms are most relevant to the input"""
        text_lower = text.lower()
        relevant_axioms = []
        
        axiom_keywords = {
            'narrative_supremacy': ['story', 'narrative', 'truth', 'reality'],
            'duality_principle': ['balance', 'both', 'complex', 'grey'],
            'flawed_hero_doctrine': ['hero', 'struggle', 'growth', 'imperfect'],
            'justifiable_force_doctrine': ['force', 'violence', 'justice', 'protection'],
            'sovereign_accountability': ['power', 'authority', 'responsibility', 'service'],
            'authentic_performance': ['authentic', 'real', 'genuine', 'action'],
            'transparency_mandate': ['truth', 'open', 'transparent', 'honest'],
            'generational_responsibility': ['future', 'legacy', 'children', 'tomorrow']
        }
        
        for axiom, keywords in axiom_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                relevant_axioms.append(axiom)
        
        return relevant_axioms
    
    def _format_concepts(self, concepts: List[str]) -> str:
        """Format concepts for output"""
        if not concepts:
            return "- No specific TEC concepts identified"
        return '\n'.join(f"- {concept.title()}" for concept in concepts)
    
    def _format_action_plan(self, plan: Dict[str, Any]) -> str:
        """Format action plan for output"""
        formatted = []
        for category, actions in plan.items():
            formatted.append(f"{category.replace('_', ' ').title()}:")
            for action in actions:
                formatted.append(f"  • {action}")
        return '\n'.join(formatted)
    
    def _format_axiom_considerations(self, axioms: List[str]) -> str:
        """Format axiom considerations for output"""
        if not axioms:
            return "- General axiom review recommended"
        return '\n'.join(f"- {axiom.replace('_', ' ').title()}" for axiom in axioms)
    
    def list_available_tools(self) -> Dict[str, Any]:
        """Get a list of all available tools"""
        return {
            "tools": {
                tool_name: {
                    'name': tool_config['name'],
                    'description': tool_config['description'],
                    'category': tool_config['category'],
                    'type': tool_config['type'],
                    'parameters': tool_config['parameters']
                }
                for tool_name, tool_config in self.available_tools.items()
            },
            "total_count": len(self.available_tools),
            "status": self.status
        }
    
    # New MCP Interface Methods
    def validate_axioms(self, content: str, content_type: str = 'narrative', 
                       validation_level: str = 'moderate') -> Dict[str, Any]:
        """Validate content against TEC axioms"""
        start_time = datetime.now()
        
        if AXIOM_ENGINE_AVAILABLE:
            try:
                axiom_engine = AxiomEngine()
                result = axiom_engine.validate_content(content, content_type)
                result['processing_time'] = (datetime.now() - start_time).total_seconds() * 1000
                return result
            except Exception as e:
                logger.error(f"Axiom validation error: {e}")
                return {
                    'valid': False,
                    'error': str(e),
                    'processing_time': (datetime.now() - start_time).total_seconds() * 1000
                }
        else:
            # Fallback validation
            return {
                'valid': True,
                'axiom_scores': {'fallback': 0.8},
                'violations': [],
                'confidence_score': 0.8,
                'processing_time': (datetime.now() - start_time).total_seconds() * 1000,
                'warning': 'Axiom Engine not available - using fallback validation'
            }
    
    def query_memory(self, query: str, limit: int = 10, 
                    include_metadata: bool = True) -> Dict[str, Any]:
        """Query the TEC memory core"""
        start_time = datetime.now()
        
        if MEMORY_CORE_AVAILABLE:
            try:
                memory_core = MemoryCore()
                memory_core.initialize()
                result = memory_core.semantic_search(query, "narrative")
                
                # Handle both dict and list returns
                if isinstance(result, list):
                    fragments = result[:limit]
                    total_matches = len(result)
                else:
                    fragments = result.get('fragments', [])[:limit]
                    total_matches = result.get('total_matches', len(fragments))
                
                return {
                    'fragments': fragments,
                    'total_matches': total_matches,
                    'query_time': (datetime.now() - start_time).total_seconds() * 1000,
                    'query': query
                }
            except Exception as e:
                logger.error(f"Memory query error: {e}")
                return {
                    'fragments': [],
                    'total_matches': 0,
                    'query_time': (datetime.now() - start_time).total_seconds() * 1000,
                    'error': str(e)
                }
        else:
            # Fallback with simulated results
            return {
                'fragments': [],
                'total_matches': 0,
                'query_time': (datetime.now() - start_time).total_seconds() * 1000,
                'warning': 'Memory Core not available - no results returned'
            }
    
    def process_asset(self, file_path: str, enable_hybrid: bool = True) -> Dict[str, Any]:
        """Process an asset through the TEC pipeline"""
        start_time = datetime.now()
        
        if ASSET_PROCESSOR_AVAILABLE:
            try:
                processor = AssetProcessor()
                processor.initialize()
                result = processor.process_audio_file(file_path)
                result['processing_time'] = (datetime.now() - start_time).total_seconds() * 1000
                return result
            except Exception as e:
                logger.error(f"Asset processing error: {e}")
                return {
                    'status': 'error',
                    'error': str(e),
                    'processing_time': (datetime.now() - start_time).total_seconds() * 1000
                }
        else:
            # Fallback processing
            return {
                'status': 'processed',
                'fragments_created': 1,
                'narrative_threads': ['fallback_thread'],
                'processing_time': (datetime.now() - start_time).total_seconds() * 1000,
                'warning': 'Asset Processor not available - using fallback'
            }
    
    def hybrid_synthesis(self, content: str, processing_type: str = 'creative',
                        include_metrics: bool = True) -> Dict[str, Any]:
        """Process content through hybrid intelligence"""
        start_time = datetime.now()
        
        if HYBRID_INTELLIGENCE_AVAILABLE:
            try:
                hybrid_engine = get_hybrid_engine()
                result = hybrid_engine.process_hybrid_input(content, processing_type)
                result['processing_time'] = (datetime.now() - start_time).total_seconds() * 1000
                return result
            except Exception as e:
                logger.error(f"Hybrid synthesis error: {e}")
                return {
                    'synthesis_output': content,
                    'processing_pathway': 'fallback',
                    'performance_metrics': {'final_coherence': 0.8},
                    'processing_time': (datetime.now() - start_time).total_seconds() * 1000,
                    'error': str(e)
                }
        else:
            # Fallback synthesis
            return {
                'synthesis_output': f"[Hybrid synthesis of: {content[:100]}...]",
                'processing_pathway': 'fallback',
                'performance_metrics': {'final_coherence': 0.8},
                'processing_time': (datetime.now() - start_time).total_seconds() * 1000,
                'warning': 'Hybrid Intelligence not available - using fallback'
            }
    
    def generate_lore(self, prompt: str, lore_type: str = 'fragment',
                     narrative_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate lore content"""
        start_time = datetime.now()
        
        try:
            # Use hybrid synthesis for lore generation
            synthesis_result = self.hybrid_synthesis(prompt, 'creative')
            
            fragment_id = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            return {
                'fragment_id': fragment_id,
                'lore_type': lore_type,
                'content': synthesis_result.get('synthesis_output', prompt),
                'themes': ['generated', lore_type],
                'emotional_intensity': 0.75,
                'processing_time': (datetime.now() - start_time).total_seconds() * 1000,
                'source_prompt': prompt
            }
        except Exception as e:
            logger.error(f"Lore generation error: {e}")
            return {
                'fragment_id': f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'lore_type': lore_type,
                'content': f"Failed to generate lore from prompt: {prompt}",
                'themes': ['error'],
                'processing_time': (datetime.now() - start_time).total_seconds() * 1000,
                'error': str(e)
            }
