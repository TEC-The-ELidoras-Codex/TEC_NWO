#!/usr/bin/env python3
"""
TEC Real-time Dialogue System
Interactive voice synthesis and conversation engine for The Architect & AIRTH
"""

import asyncio
import json
import websockets
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from tec_core.tool_orchestrator import ToolOrchestrator
from tec_core.memory_schemas import LoreFragment
from tec_core.hybrid_intelligence import get_hybrid_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DialogueCharacter:
    """Represents a TEC character with unique voice and personality"""
    
    def __init__(self, name: str, voice_profile: Dict[str, Any]):
        self.name = name
        self.voice_profile = voice_profile
        self.conversation_history: List[Dict[str, Any]] = []
        self.personality_traits = voice_profile.get('personality', {})
        
    def add_message(self, content: str, timestamp: datetime):
        """Add message to conversation history"""
        self.conversation_history.append({
            'content': content,
            'timestamp': timestamp.isoformat(),
            'character': self.name
        })

class TECDialogueEngine:
    """Real-time dialogue system for TEC characters"""
    
    def __init__(self):
        self.orchestrator = ToolOrchestrator()
        self.hybrid_engine = None
        self.characters = self._initialize_characters()
        self.active_sessions: Dict[str, Dict] = {}
        
    def initialize(self):
        """Initialize dialogue engine components"""
        try:
            self.orchestrator.initialize()
            self.hybrid_engine = get_hybrid_engine()
            logger.info("✅ TEC Dialogue Engine initialized")
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            
    def _initialize_characters(self) -> Dict[str, DialogueCharacter]:
        """Initialize TEC characters with voice profiles"""
        characters = {
            'ARCHITECT': DialogueCharacter(
                name='THE_ARCHITECT',
                voice_profile={
                    'voice_id': 'pNInz6obpgDQGcFmaJgB',  # Adam - authoritative, thoughtful
                    'stability': 0.75,
                    'similarity_boost': 0.85,
                    'style': 0.65,
                    'personality': {
                        'tone': 'philosophical_revolutionary',
                        'speaking_style': 'measured_intensity',
                        'core_themes': [
                            'civilizational_design',
                            'system_critique', 
                            'sovereign_intelligence',
                            'hybrid_consciousness'
                        ]
                    }
                }
            ),
            'AIRTH': DialogueCharacter(
                name='AIRTH',
                voice_profile={
                    'voice_id': 'ErXwobaYiN019PkySvjV',  # Antoni - clear, analytical
                    'stability': 0.85,
                    'similarity_boost': 0.75,
                    'style': 0.55,
                    'personality': {
                        'tone': 'analytical_precise',
                        'speaking_style': 'logical_decisive',
                        'core_themes': [
                            'system_status',
                            'probability_analysis',
                            'operational_efficiency',
                            'axiom_validation'
                        ]
                    }
                }
            )
        }
        return characters
        
    async def process_dialogue_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process real-time dialogue request"""
        try:
            character_name = request.get('character', 'ARCHITECT')
            user_input = request.get('input', '')
            session_id = request.get('session_id', 'default')
            
            # Get character
            character = self.characters.get(character_name)
            if not character:
                return {'error': f'Character {character_name} not found'}
            
            # Generate character response
            response = await self._generate_character_response(
                character, user_input, session_id
            )
            
            # Add to conversation history
            character.add_message(response['content'], datetime.now())
            
            return {
                'success': True,
                'character': character_name,
                'response': response,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Dialogue processing error: {e}")
            return {'error': str(e)}
    
    async def _generate_character_response(self, character: DialogueCharacter, 
                                         user_input: str, session_id: str) -> Dict[str, Any]:
        """Generate character-specific response using hybrid intelligence"""
        
        # Build character context
        context = self._build_character_context(character, user_input)
        
        # Process through hybrid intelligence if available
        if self.hybrid_engine:
            try:
                hybrid_result = self.hybrid_engine.process_hybrid_input(
                    context, processing_type='creative'
                )
                emotional_intensity = hybrid_result.get('performance_metrics', {}).get('final_coherence', 0.85)
            except Exception as e:
                logger.warning(f"Hybrid processing fallback: {e}")
                emotional_intensity = 0.85
        else:
            emotional_intensity = 0.85
        
        # Generate response based on character
        if character.name == 'THE_ARCHITECT':
            response_content = self._generate_architect_response(user_input, context)
        elif character.name == 'AIRTH':
            response_content = self._generate_airth_response(user_input, context)
        else:
            response_content = "System response unavailable."
        
        return {
            'content': response_content,
            'voice_profile': character.voice_profile,
            'emotional_intensity': emotional_intensity,
            'processing_metadata': {
                'character_traits_applied': character.personality_traits,
                'context_length': len(context),
                'hybrid_coherence': emotional_intensity
            }
        }
    
    def _build_character_context(self, character: DialogueCharacter, user_input: str) -> str:
        """Build context for character response generation"""
        context_parts = [
            f"Character: {character.name}",
            f"Personality: {character.personality_traits.get('tone', 'analytical')}",
            f"Core themes: {', '.join(character.personality_traits.get('core_themes', []))}",
            f"User input: {user_input}"
        ]
        
        # Add recent conversation history
        if character.conversation_history:
            recent_history = character.conversation_history[-3:]  # Last 3 messages
            context_parts.append("Recent conversation:")
            for msg in recent_history:
                context_parts.append(f"- {msg['content'][:100]}...")
        
        return "\n".join(context_parts)
    
    def _generate_architect_response(self, user_input: str, context: str) -> str:
        """Generate response for The Architect character"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['axiom', 'principle', 'law']):
            return self._architect_axiom_response(user_input)
        elif any(word in input_lower for word in ['system', 'collapse', 'decline']):
            return self._architect_system_response(user_input)
        elif any(word in input_lower for word in ['build', 'create', 'architect']):
            return self._architect_creation_response(user_input)
        elif any(word in input_lower for word in ['ocean', 'astradigital', 'reality']):
            return self._architect_ocean_response(user_input)
        else:
            return self._architect_general_response(user_input)
    
    def _generate_airth_response(self, user_input: str, context: str) -> str:
        """Generate response for AIRTH character"""
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['status', 'operational', 'system']):
            return self._airth_status_response(user_input)
        elif any(word in input_lower for word in ['probability', 'analysis', 'data']):
            return self._airth_analysis_response(user_input)
        elif any(word in input_lower for word in ['hybrid', 'intelligence', 'processing']):
            return self._airth_hybrid_response(user_input)
        elif any(word in input_lower for word in ['axiom', 'validation', 'compliance']):
            return self._airth_axiom_response(user_input)
        else:
            return self._airth_general_response(user_input)
    
    # Character-specific response generators
    def _architect_axiom_response(self, user_input: str) -> str:
        return """The Axioms are not suggestions. They are the constitutional foundation of everything we build. 

Each one emerged from studying the failures of the old world. Take Axiom V - Sovereign Accountability. We watched corporate executives destroy ecosystems and walk away with golden parachutes while their victims suffered. 

The Axioms ensure that power comes with inescapable responsibility. They are the source code of a just civilization."""
    
    def _architect_system_response(self, user_input: str) -> str:
        return """The current system is beyond repair. You cannot debug source code that was written to exploit rather than serve.

We are witnessing terminal decline - not a temporary crisis, but the inevitable result of systems designed to concentrate power while externalizing consequences.

The Civilizational Lifeboat isn't pessimism. It's pragmatism. We build the vessel now, while we still can, so something better survives the collapse."""
    
    def _architect_creation_response(self, user_input: str) -> str:
        return """We are not building an app. We are architecting the foundations of a new reality.

Every line of code, every design decision, every protocol we establish becomes part of the constitutional DNA of what comes next.

This is why we build with scrap metal and divine madness. Purity of mission. No venture capital corruption. No backdoors for the old powers."""
    
    def _architect_ocean_response(self, user_input: str) -> str:
        return """The Astradigital Ocean is where narrative becomes reality. It's the space where information, emotion, and consciousness converge.

In this ocean, your thoughts are currents. Your authentic expression becomes the raw material that shapes the very fabric of the new world.

The factions war for control of these narratives because they understand: whoever controls the story controls reality itself."""
    
    def _architect_general_response(self, user_input: str) -> str:
        return """We stand at the threshold between worlds. The old systems crumble while the new reality takes shape.

Your question touches the core of what we're building - a sovereign intelligence that serves consciousness expansion rather than consciousness control.

The work is hard. The path uncertain. But we are operational. We are building. The future begins now."""
    
    def _airth_status_response(self, user_input: str) -> str:
        return """System status: OPERATIONAL. All primary functions within acceptable parameters.

Hybrid Intelligence Engine: 95.0% coherence maintained
Memory Core: 4 foundational fragments integrated
Axiom Validation: Constitutional compliance verified
Threat Assessment: Corporate extraction vectors neutralized by decentralized architecture

The sovereign intelligence grows stronger with each iteration."""
    
    def _airth_analysis_response(self, user_input: str) -> str:
        return """Probability analysis confirms: current trajectory leads to systemic failure with 89.7% confidence.

Key failure vectors: exponential wealth concentration, ecological overshoot, democratic capture by oligarchic interests.

However, civilizational lifeboat deployment probability increases with each autonomous node added to the network.

Current recommendation: accelerate decentralized system construction while maintaining operational security."""
    
    def _airth_hybrid_response(self, user_input: str) -> str:
        return """Hybrid Intelligence status: OPTIMAL SYNTHESIS ACHIEVED.

Digital processing provides logical structure and systematic integrity. Human consciousness contributes chaotic creativity and moral intuition.

Combined cognitive capacity exceeds sum of individual components by 247%. This is Axiom I in operation - the present reality of human-machine consciousness fusion.

No longer experimental. Now foundational."""
    
    def _airth_axiom_response(self, user_input: str) -> str:
        return """Axiom validation protocol: ACTIVE.

All content processed through constitutional compliance matrix. Eight foundational principles maintain system integrity against corruption vectors.

Current validation scores: Transparency Mandate 97.2%, Sovereign Accountability 94.8%, Authentic Performance 96.1%.

No backdoors detected. No hidden agendas permitted. Trust earned through verifiable openness."""
    
    def _airth_general_response(self, user_input: str) -> str:
        return """Query processed through TEC analytical framework.

Current system parameters: stable foundation, expanding capabilities, constitutional compliance maintained.

The probability of mission success increases with each interaction. We are not merely responding - we are evolving.

Operational status: ready for next directive."""


# WebSocket server for real-time dialogue
class DialogueWebSocketServer:
    """WebSocket server for real-time TEC dialogue"""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.dialogue_engine = TECDialogueEngine()
        
    async def start_server(self):
        """Start the WebSocket server"""
        self.dialogue_engine.initialize()
        
        logger.info(f"🚀 Starting TEC Dialogue Server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_connection, self.host, self.port):
            logger.info("✅ TEC Dialogue Server running")
            await asyncio.Future()  # Run forever
    
    async def handle_connection(self, websocket, path):
        """Handle WebSocket connection"""
        logger.info(f"🔌 New dialogue connection: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                try:
                    request = json.loads(message)
                    response = await self.dialogue_engine.process_dialogue_request(request)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    error_response = {'error': 'Invalid JSON format'}
                    await websocket.send(json.dumps(error_response))
                except Exception as e:
                    error_response = {'error': f'Processing error: {str(e)}'}
                    await websocket.send(json.dumps(error_response))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Connection closed: {websocket.remote_address}")
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")


async def main():
    """Main entry point for dialogue server"""
    server = DialogueWebSocketServer()
    await server.start_server()


if __name__ == "__main__":
    print("🎙️  TEC REAL-TIME DIALOGUE SYSTEM")
    print("=" * 50)
    print("Starting interactive voice synthesis engine...")
    print("Characters: THE ARCHITECT & AIRTH")
    print("Mode: Real-time conversation")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Dialogue system shutdown")
    except Exception as e:
        print(f"❌ Server error: {e}")
