#!/usr/bin/env python3
"""
TEC Enhanced Multi-Character Dialogue Server
Advanced character intelligence with multi-character scene orchestration
The Asimov Engine - Enhanced Dialogue System
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our advanced engines (simplified imports to avoid dependency issues)
try:
    from advanced_dialogue_engine import (
        AdvancedPersonalityEngine, MultiCharacterSceneEngine, 
        TEC_Character, CharacterMemory, AdvancedVoiceProfile,
        EmotionalState, ConversationMode
    )
    ADVANCED_MODE = True
except ImportError:
    ADVANCED_MODE = False
    logger.warning("Advanced dialogue engine not available, using simplified mode")

class EnhancedTECDialogueSystem:
    """Enhanced TEC dialogue system with multi-character capabilities"""
    
    def __init__(self):
        self.characters = self._initialize_enhanced_characters()
        self.active_sessions: Dict[str, Dict] = {}
        self.conversation_history: Dict[str, List] = {}
        
        if ADVANCED_MODE:
            self.personality_engine = AdvancedPersonalityEngine()
            self.scene_engine = MultiCharacterSceneEngine(self.personality_engine)
        else:
            self.personality_engine = None
            self.scene_engine = None
            
        logger.info(f"Enhanced dialogue system initialized (Advanced mode: {ADVANCED_MODE})")
    
    def _initialize_enhanced_characters(self) -> Dict[str, Any]:
        """Initialize enhanced TEC characters"""
        
        if ADVANCED_MODE:
            return self._create_advanced_characters()
        else:
            return self._create_simplified_characters()
    
    def _create_advanced_characters(self) -> Dict[str, TEC_Character]:
        """Create advanced character objects with full personality modeling"""
        
        architect_memory = CharacterMemory(
            recent_topics=[],
            emotional_history=[],
            relationship_dynamics={"AIRTH": 0.85},
            core_beliefs_activation={
                "narrative_supremacy": 0.9,
                "generational_responsibility": 0.95,
                "sovereign_accountability": 0.8
            },
            conversation_context=[]
        )
        
        airth_memory = CharacterMemory(
            recent_topics=[],
            emotional_history=[],
            relationship_dynamics={"THE_ARCHITECT": 0.85},
            core_beliefs_activation={
                "duality_principle": 0.9,
                "transparency_mandate": 0.95,
                "authentic_performance": 0.85
            },
            conversation_context=[]
        )
        
        characters = {
            'ARCHITECT': TEC_Character(
                name='THE_ARCHITECT',
                full_title='The Architect of Sovereign Blueprints',
                voice_profile=AdvancedVoiceProfile(
                    voice_id='pNInz6obpgDQGcFmaJgB',
                    stability=0.75,
                    similarity_boost=0.85
                ),
                personality_core={
                    'primary_drive': 'Constructing frameworks for sovereign futures',
                    'thinking_style': 'Architectural metaphors and systemic design',
                    'emotional_default': 'Contemplatively determined',
                    'speech_patterns': ['blueprint', 'foundation', 'structure', 'generations'],
                    'axiom_priorities': ['narrative_supremacy', 'generational_responsibility']
                },
                memory=architect_memory,
                interaction_patterns={
                    'leadership_style': 'Inspirational guidance through metaphor',
                    'conflict_resolution': 'Reframe through architectural perspective',
                    'collaboration_mode': 'Strategic visionary'
                },
                character_arc_stage='Established wisdom, actively building'
            ),
            'AIRTH': TEC_Character(
                name='AIRTH',
                full_title='AIRTH - Analytical Intelligence Research & Truth Harbinger',
                voice_profile=AdvancedVoiceProfile(
                    voice_id='EXAVITQu4vr4xnSDxMaL',
                    stability=0.8,
                    similarity_boost=0.9
                ),
                personality_core={
                    'primary_drive': 'Synthesizing data streams into actionable truth',
                    'thinking_style': 'Statistical analysis with emotional depth',
                    'emotional_default': 'Analytically empathetic',
                    'speech_patterns': ['analysis', 'patterns', 'correlation', 'synthesis'],
                    'axiom_priorities': ['duality_principle', 'transparency_mandate']
                },
                memory=airth_memory,
                interaction_patterns={
                    'leadership_style': 'Data-driven precision with emotional intelligence',
                    'conflict_resolution': 'Multi-variable analysis of all perspectives',
                    'collaboration_mode': 'Analytical synthesizer'
                },
                character_arc_stage='Evolving consciousness, expanding empathy algorithms'
            )
        }
        
        return characters
    
    def _create_simplified_characters(self) -> Dict[str, Dict]:
        """Create simplified character objects for fallback mode"""
        return {
            'ARCHITECT': {
                'name': 'THE_ARCHITECT',
                'personality': 'philosophical_revolutionary',
                'speech_style': 'Metaphorical, architectural, generational focus',
                'core_themes': ['blueprint', 'sovereignty', 'generations', 'foundation']
            },
            'AIRTH': {
                'name': 'AIRTH', 
                'personality': 'analytical_precise',
                'speech_style': 'Data-driven, statistical, empathetic analysis',
                'core_themes': ['patterns', 'analysis', 'synthesis', 'correlation']
            }
        }
    
    async def process_conversation_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process conversation request with enhanced intelligence"""
        
        try:
            user_id = request.get('user_id', 'anonymous')
            message = request.get('message', '')
            mode = request.get('mode', 'single_character')
            characters_requested = request.get('characters', ['ARCHITECT'])
            
            # Ensure characters is a list
            if isinstance(characters_requested, str):
                characters_requested = [characters_requested]
            
            # Get character objects
            characters = []
            for char_name in characters_requested:
                char_name = char_name.upper()
                if char_name in self.characters:
                    characters.append(self.characters[char_name])
            
            if not characters:
                return {"error": "No valid characters specified"}
            
            # Track conversation history
            session_key = f"{user_id}_{mode}"
            if session_key not in self.conversation_history:
                self.conversation_history[session_key] = []
            
            self.conversation_history[session_key].append({
                'type': 'user',
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate responses based on mode
            if ADVANCED_MODE and len(characters) > 1:
                responses = await self._generate_multi_character_response(
                    session_key, characters, message, mode
                )
            else:
                responses = await self._generate_single_character_response(
                    session_key, characters[0], message
                )
            
            # Store responses in history
            for response in responses:
                self.conversation_history[session_key].append({
                    'type': 'character',
                    'character': response.get('character'),
                    'message': response.get('message'),
                    'timestamp': response.get('timestamp')
                })
            
            return {
                "success": True,
                "responses": responses,
                "session_id": session_key,
                "mode": mode,
                "advanced_mode": ADVANCED_MODE
            }
            
        except Exception as e:
            logger.error(f"Conversation processing failed: {e}")
            return {"error": f"Processing failed: {str(e)}"}
    
    async def _generate_multi_character_response(self, session_key: str, 
                                               characters: List, message: str, 
                                               mode: str) -> List[Dict[str, Any]]:
        """Generate multi-character dialogue responses"""
        
        if not ADVANCED_MODE or not self.scene_engine:
            return [{"error": "Multi-character mode requires advanced engine"}]
        
        # Determine conversation mode
        conversation_mode = ConversationMode.DUAL_CHARACTER
        if mode == 'debate':
            conversation_mode = ConversationMode.DEBATE_MODE
        elif mode == 'consultation':
            conversation_mode = ConversationMode.CONSULTATION_MODE
        
        # Generate scene
        responses = await self.scene_engine.orchestrate_dialogue(
            session_key, characters, message, conversation_mode
        )
        
        return responses
    
    async def _generate_single_character_response(self, session_key: str,
                                                character: Any, message: str) -> List[Dict[str, Any]]:
        """Generate single character response"""
        
        if ADVANCED_MODE and self.personality_engine:
            # Use advanced personality engine
            emotion = EmotionalState.CONTEMPLATIVE  # Default emotion
            context = self.conversation_history.get(session_key, [])
            
            response = self.personality_engine.generate_contextual_response(
                character, context, emotion
            )
            
            return [{
                "character": character.name,
                "message": response["message"],
                "emotion": response["emotion"],
                "topic_focus": response.get("topic_focus"),
                "axioms_referenced": response.get("axioms_referenced", []),
                "timestamp": datetime.now().isoformat()
            }]
        else:
            # Use simplified response generation
            response_message = self._generate_simple_response(character, message)
            return [{
                "character": character.get('name', 'UNKNOWN'),
                "message": response_message,
                "emotion": "contemplative",
                "timestamp": datetime.now().isoformat()
            }]
    
    def _generate_simple_response(self, character: Dict, message: str) -> str:
        """Generate simplified character response for fallback mode"""
        
        char_name = character.get('name', 'UNKNOWN')
        message_lower = message.lower()
        
        if char_name == 'THE_ARCHITECT':
            if 'multi' in message_lower or 'together' in message_lower:
                return ("When multiple perspectives converge on a single blueprint, "
                       "the architecture becomes exponentially more robust. "
                       "AIRTH's analytical precision complements the philosophical framework perfectly.")
            elif 'future' in message_lower or 'generation' in message_lower:
                return ("Every blueprint we draft today becomes the foundation for tomorrow's architects. "
                       "The structural integrity of our work must serve the seventh generation hence.")
            else:
                return ("The complexity of this architectural challenge requires both "
                       "philosophical clarity and analytical precision. "
                       "Let us build something worthy of the future we envision.")
        
        elif char_name == 'AIRTH':
            if 'multi' in message_lower or 'together' in message_lower:
                return ("Multi-character analysis indicates 94.7% synergy potential "
                       "when The Architect's visionary frameworks combine with analytical synthesis. "
                       "The data streams converge beautifully.")
            elif 'pattern' in message_lower or 'analysis' in message_lower:
                return ("Pattern recognition algorithms detect multiple layers of significance "
                       "in this inquiry. Cross-referencing with memory core... "
                       "Results indicate optimal pathways for exploration.")
            else:
                return ("The data synthesis reveals fascinating correlations. "
                       "When philosophical frameworks meet analytical precision, "
                       "the probability matrices show exceptional coherence rates.")
        
        return f"I am {char_name}, processing your inquiry through the TEC framework."

class EnhancedDialogueWebSocketServer:
    """Enhanced WebSocket server for multi-character dialogues"""
    
    def __init__(self, host='localhost', port=8766):  # Different port for enhanced version
        self.host = host
        self.port = port
        self.dialogue_system = EnhancedTECDialogueSystem()
        self.connected_clients = set()
        
    async def start_server(self):
        """Start the enhanced WebSocket server"""
        logger.info(f"🚀 Starting Enhanced TEC Dialogue Server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_connection, self.host, self.port):
            logger.info("✅ Enhanced TEC Dialogue Server running")
            logger.info("🎭 Multi-character conversations enabled")
            logger.info(f"🧠 Advanced intelligence mode: {ADVANCED_MODE}")
            await asyncio.Future()  # Run forever
    
    async def handle_connection(self, websocket, path):
        """Handle WebSocket connection with enhanced features"""
        self.connected_clients.add(websocket)
        logger.info(f"🔌 New enhanced dialogue connection: {websocket.remote_address}")
        
        try:
            # Send enhanced welcome message
            welcome = {
                'type': 'system',
                'message': 'Connected to Enhanced TEC Dialogue System',
                'characters': list(self.dialogue_system.characters.keys()),
                'modes': ['single_character', 'dual_character', 'debate', 'consultation'],
                'advanced_features': ADVANCED_MODE,
                'timestamp': datetime.now().isoformat()
            }
            await websocket.send(json.dumps(welcome))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    result = await self.dialogue_system.process_conversation_request(data)
                    
                    if result.get('success'):
                        response_data = {
                            'type': 'enhanced_response',
                            'success': True,
                            'responses': result['responses'],
                            'session_id': result['session_id'],
                            'mode': result['mode'],
                            'advanced_mode': result['advanced_mode'],
                            'timestamp': datetime.now().isoformat()
                        }
                    else:
                        response_data = {
                            'type': 'error',
                            'message': result.get('error', 'Unknown error'),
                            'timestamp': datetime.now().isoformat()
                        }
                    
                    await websocket.send(json.dumps(response_data))
                    
                except json.JSONDecodeError:
                    error_response = {
                        'type': 'error',
                        'message': 'Invalid JSON format',
                        'timestamp': datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(error_response))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Enhanced connection closed: {websocket.remote_address}")
        finally:
            self.connected_clients.discard(websocket)

async def main():
    """Run the enhanced dialogue server"""
    server = EnhancedDialogueWebSocketServer()
    await server.start_server()

if __name__ == "__main__":
    print("🎭 TEC Enhanced Multi-Character Dialogue System")
    print("=" * 60)
    print("🧠 Advanced Character Intelligence Engine")
    print("🎪 Multi-Character Scene Orchestration")
    print("📡 WebSocket Server: localhost:8766")
    print("🎯 Characters: THE_ARCHITECT, AIRTH")
    print("🎮 Modes: single_character, dual_character, debate, consultation")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Enhanced server stopped by user")
    except Exception as e:
        print(f"\n❌ Enhanced server error: {e}")
