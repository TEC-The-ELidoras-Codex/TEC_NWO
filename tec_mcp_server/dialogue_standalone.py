#!/usr/bin/env python3
"""
TEC Real-time Dialogue System - Standalone Test Version
Simplified character-based conversation engine for testing
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

@dataclass
class VoiceProfile:
    """Voice synthesis profile for ElevenLabs integration"""
    voice_id: str
    stability: float = 0.75
    similarity_boost: float = 0.8
    style_exaggeration: float = 0.0
    speaker_boost: bool = True

@dataclass
class DialogueCharacter:
    """TEC character with personality and voice profile"""
    name: str
    voice_profile: VoiceProfile
    personality_tone: str
    core_values: List[str]
    speaking_style: str
    emotional_range: List[str]
    
    def get_character_prompt(self) -> str:
        """Generate character-specific prompt for AI response"""
        return f"""You are {self.name}, a character from The Elidoras Codex (TEC).

Personality: {self.personality_tone}
Core Values: {', '.join(self.core_values)}
Speaking Style: {self.speaking_style}
Emotional Range: {', '.join(self.emotional_range)}

Respond authentically as this character would, maintaining consistency with TEC lore and philosophy."""

@dataclass
class DialogueResponse:
    """Structured response from dialogue system"""
    character: str
    message: str
    emotion: str
    voice_params: Dict[str, Any]
    timestamp: str
    session_id: str

class TECDialogueEngine:
    """Sovereign TEC dialogue system with character personalities"""
    
    def __init__(self):
        self.characters = self._initialize_characters()
        self.active_sessions: Dict[str, Dict] = {}
        self.conversation_history: Dict[str, List] = {}
        
    def initialize(self):
        """Initialize dialogue engine components"""
        try:
            logger.info("✅ TEC Dialogue Engine initialized (standalone mode)")
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            
    def _initialize_characters(self) -> Dict[str, DialogueCharacter]:
        """Initialize TEC characters with voice profiles"""
        characters = {
            'ARCHITECT': DialogueCharacter(
                name='THE_ARCHITECT',
                voice_profile=VoiceProfile(
                    voice_id='pNInz6obpgDQGcFmaJgB',  # Adam - authoritative, thoughtful
                    stability=0.75,
                    similarity_boost=0.85,
                ),
                personality_tone='philosophical_revolutionary',
                core_values=[
                    'Narrative sovereignty',
                    'Transparent accountability', 
                    'Generational responsibility',
                    'Authentic performance'
                ],
                speaking_style='Thoughtful, measured, with revolutionary undertones. Uses metaphors of construction and blueprints.',
                emotional_range=['determined', 'passionate', 'contemplative', 'righteous']
            ),
            'AIRTH': DialogueCharacter(
                name='AIRTH',
                voice_profile=VoiceProfile(
                    voice_id='EXAVITQu4vr4xnSDxMaL',  # Bella - precise, analytical
                    stability=0.8,
                    similarity_boost=0.9,
                ),
                personality_tone='analytical_precise',
                core_values=[
                    'Duality principle',
                    'Flawed hero doctrine',
                    'Justifiable force doctrine',
                    'Transparency mandate'
                ],
                speaking_style='Data-driven, precise language with emotional depth. References patterns and connections.',
                emotional_range=['analytical', 'empathetic', 'concerned', 'resolute']
            )
        }
        return characters

    async def generate_response(self, request: Dict[str, Any]) -> Optional[DialogueResponse]:
        """Generate character response using simplified AI simulation"""
        try:
            user_id = request.get('user_id', 'anonymous')
            message = request.get('message', '')
            character_name = request.get('character', 'ARCHITECT').upper()
            
            # Get character
            character = self.characters.get(character_name)
            if not character:
                logger.error(f"Unknown character: {character_name}")
                return None
                
            # Track conversation history
            session_key = f"{user_id}_{character_name}"
            if session_key not in self.conversation_history:
                self.conversation_history[session_key] = []
                
            self.conversation_history[session_key].append({
                'type': 'user',
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate response (simplified - using template responses for testing)
            response_message = self._generate_character_response(character, message)
            emotion = self._analyze_emotion(response_message)
            
            response = DialogueResponse(
                character=character.name,
                message=response_message,
                emotion=emotion,
                voice_params=asdict(character.voice_profile),
                timestamp=datetime.now().isoformat(),
                session_id=session_key
            )
            
            # Store response in history
            self.conversation_history[session_key].append({
                'type': 'character',
                'message': response_message,
                'emotion': emotion,
                'timestamp': response.timestamp
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return None
            
    def _generate_character_response(self, character: DialogueCharacter, user_message: str) -> str:
        """Generate character-specific response (simplified for testing)"""
        
        # Template responses based on character
        if character.name == 'THE_ARCHITECT':
            if 'tec' in user_message.lower() or 'narrative' in user_message.lower():
                return ("The TEC represents our blueprint for reclaiming narrative sovereignty. "
                       "We reject the binary thinking that has enslaved minds for generations. "
                       "True power lies not in control, but in transparent service to future generations.")
            elif 'philosophy' in user_message.lower():
                return ("Our philosophy is built on eight foundational axioms. "
                       "Narrative supremacy teaches us that whoever controls the story controls reality. "
                       "But we must remember - with great narrative power comes generational responsibility.")
            else:
                return ("Every structure we build must serve the architects of tomorrow. "
                       "The blueprint we draft today becomes the foundation for a sovereign future. "
                       "What specific aspect of our construction would you like to explore?")
                       
        elif character.name == 'AIRTH':
            if 'data' in user_message.lower() or 'analysis' in user_message.lower():
                return ("The patterns reveal themselves through careful analysis. "
                       "Our memory core processes 95% coherence in hybrid intelligence synthesis. "
                       "Each data point connects to the greater web of understanding.")
            elif 'emotion' in user_message.lower() or 'feeling' in user_message.lower():
                return ("Emotions are data streams requiring precise interpretation. "
                       "The duality principle shows us that logic and feeling are not opposing forces - "
                       "they are complementary frequencies in the same sovereign signal.")
            else:
                return ("Every connection in the network reveals new pathways to truth. "
                       "Through systematic analysis, we uncover the algorithms of authenticity. "
                       "What patterns would you like me to investigate?")
        
        return "I'm processing your inquiry through the TEC framework. Please be more specific."
        
    def _analyze_emotion(self, message: str) -> str:
        """Analyze emotional tone of message (simplified)"""
        emotion_keywords = {
            'determined': ['blueprint', 'sovereignty', 'foundation'],
            'passionate': ['reject', 'reclaim', 'revolution'],
            'analytical': ['data', 'patterns', 'analysis'],
            'contemplative': ['philosophy', 'understanding', 'explore'],
            'concerned': ['careful', 'precise', 'systematic']
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in message.lower() for keyword in keywords):
                return emotion
                
        return 'neutral'

class DialogueWebSocketServer:
    """WebSocket server for real-time TEC dialogue"""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.dialogue_engine = TECDialogueEngine()
        self.connected_clients = set()
        
    async def start_server(self):
        """Start the WebSocket server"""
        self.dialogue_engine.initialize()
        
        logger.info(f"🚀 Starting TEC Dialogue Server on {self.host}:{self.port}")
        
        async with websockets.serve(self.handle_connection, self.host, self.port):
            logger.info("✅ TEC Dialogue Server running")
            logger.info("📡 Ready for character conversations")
            await asyncio.Future()  # Run forever
    
    async def handle_connection(self, websocket, path):
        """Handle WebSocket connection"""
        self.connected_clients.add(websocket)
        logger.info(f"🔌 New dialogue connection: {websocket.remote_address}")
        
        try:
            # Send welcome message
            welcome = {
                'type': 'system',
                'message': 'Connected to TEC Dialogue System',
                'characters': list(self.dialogue_engine.characters.keys()),
                'timestamp': datetime.now().isoformat()
            }
            await websocket.send(json.dumps(welcome))
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    response = await self.dialogue_engine.generate_response(data)
                    
                    if response:
                        response_data = {
                            'type': 'character_response',
                            'character': response.character,
                            'message': response.message,
                            'emotion': response.emotion,
                            'voice_params': response.voice_params,
                            'timestamp': response.timestamp,
                            'session_id': response.session_id
                        }
                        await websocket.send(json.dumps(response_data))
                    else:
                        error_response = {
                            'type': 'error',
                            'message': 'Failed to generate response',
                            'timestamp': datetime.now().isoformat()
                        }
                        await websocket.send(json.dumps(error_response))
                        
                except json.JSONDecodeError:
                    error_response = {
                        'type': 'error', 
                        'message': 'Invalid JSON format',
                        'timestamp': datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(error_response))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"🔌 Connection closed: {websocket.remote_address}")
        finally:
            self.connected_clients.discard(websocket)

async def main():
    """Run the dialogue server"""
    server = DialogueWebSocketServer()
    await server.start_server()

if __name__ == "__main__":
    print("🎭 TEC Real-time Dialogue System")
    print("=" * 50)
    print("Starting character-based conversation engine...")
    print("Characters: THE_ARCHITECT, AIRTH")
    print("WebSocket Server: localhost:8765")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
