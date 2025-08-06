#!/usr/bin/env python3
"""
Enhanced TEC Dialogue Test Client
Multi-character conversation testing with advanced scenarios
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional

class EnhancedDialogueClient:
    """Enhanced test client for multi-character TEC dialogue system"""
    
    def __init__(self, uri='ws://localhost:8766'):
        self.uri = uri
        self.user_id = 'enhanced_test_user'
        
    async def connect_and_test(self):
        """Connect to enhanced server and run comprehensive tests"""
        try:
            async with websockets.connect(self.uri) as websocket:
                print("✅ Connected to Enhanced TEC Dialogue Server")
                
                # Listen for welcome message
                welcome = await websocket.recv()
                welcome_data = json.loads(welcome)
                print(f"📡 {welcome_data.get('message')}")
                print(f"🎭 Available characters: {', '.join(welcome_data.get('characters', []))}")
                print(f"🎮 Available modes: {', '.join(welcome_data.get('modes', []))}")
                print(f"🧠 Advanced features: {welcome_data.get('advanced_features')}")
                
                # Run comprehensive test scenarios
                await self.run_enhanced_scenarios(websocket)
                
        except websockets.exceptions.ConnectionRefused:
            print("❌ Cannot connect to enhanced dialogue server. Is it running on localhost:8766?")
        except Exception as e:
            print(f"❌ Connection error: {e}")
    
    async def run_enhanced_scenarios(self, websocket):
        """Run enhanced test scenarios including multi-character dialogues"""
        
        scenarios = [
            {
                'name': 'Single Character - ARCHITECT',
                'request': {
                    'user_id': self.user_id,
                    'message': 'What is your vision for the blueprint of tomorrow?',
                    'characters': ['ARCHITECT'],
                    'mode': 'single_character'
                },
                'expected_count': 1
            },
            {
                'name': 'Single Character - AIRTH',
                'request': {
                    'user_id': self.user_id,
                    'message': 'Analyze the patterns in our conversation data',
                    'characters': ['AIRTH'],
                    'mode': 'single_character'
                },
                'expected_count': 1
            },
            {
                'name': 'Dual Character Dialogue',
                'request': {
                    'user_id': self.user_id,
                    'message': 'How should we approach the challenge of narrative sovereignty in the digital age?',
                    'characters': ['ARCHITECT', 'AIRTH'],
                    'mode': 'dual_character'
                },
                'expected_count': 2
            },
            {
                'name': 'Consultation Mode',
                'request': {
                    'user_id': self.user_id,
                    'message': 'We need advice on building a decentralized truth verification system',
                    'characters': ['ARCHITECT', 'AIRTH'],
                    'mode': 'consultation'
                },
                'expected_count': 2
            },
            {
                'name': 'Debate Mode',
                'request': {
                    'user_id': self.user_id,
                    'message': 'Should AI systems prioritize efficiency or transparency?',
                    'characters': ['ARCHITECT', 'AIRTH'],
                    'mode': 'debate'
                },
                'expected_count': 2
            },
            {
                'name': 'Complex Multi-Character Scene',
                'request': {
                    'user_id': self.user_id,
                    'message': 'The corporate metaverse is trying to control human consciousness through immersive narrative manipulation. How do we counter this threat while building our own sovereign digital reality?',
                    'characters': ['ARCHITECT', 'AIRTH'],
                    'mode': 'dual_character'
                },
                'expected_count': 3  # Expect synthesis response for complex topics
            }
        ]
        
        print("\n🧪 Running Enhanced Test Scenarios")
        print("=" * 60)
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎯 Test {i}: {scenario['name']}")
            print(f"   Request: {scenario['request']['message'][:60]}...")
            print(f"   Mode: {scenario['request']['mode']}")
            print(f"   Characters: {', '.join(scenario['request']['characters'])}")
            
            # Send request
            await websocket.send(json.dumps(scenario['request']))
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get('type') == 'enhanced_response' and response_data.get('success'):
                responses = response_data.get('responses', [])
                mode = response_data.get('mode')
                advanced_mode = response_data.get('advanced_mode')
                
                print(f"   ✅ Success! Mode: {mode}, Advanced: {advanced_mode}")
                print(f"   📊 Responses received: {len(responses)}")
                
                for j, resp in enumerate(responses, 1):
                    character = resp.get('character', 'UNKNOWN')
                    emotion = resp.get('emotion', 'neutral')
                    message = resp.get('message', '')
                    interaction_type = resp.get('interaction_type', 'standard')
                    
                    print(f"      {j}. {character} ({emotion}): {message[:80]}...")
                    if interaction_type != 'standard':
                        print(f"         Interaction: {interaction_type}")
                    
                    # Check for advanced features
                    if 'axioms_referenced' in resp:
                        axioms = resp['axioms_referenced']
                        if axioms:
                            print(f"         Axioms: {', '.join(axioms)}")
                    
                    if 'topic_focus' in resp:
                        print(f"         Topic: {resp['topic_focus']}")
                
                # Validate response count
                if len(responses) >= scenario['expected_count']:
                    print(f"   🎯 Response count validated ({len(responses)} >= {scenario['expected_count']})")
                else:
                    print(f"   ⚠️  Expected {scenario['expected_count']} responses, got {len(responses)}")
                    
            else:
                error_msg = response_data.get('message', 'Unknown error')
                print(f"   ❌ Error: {error_msg}")
            
            await asyncio.sleep(2)  # Pause between tests
        
        print("\n" + "=" * 60)
        print("✅ All enhanced test scenarios completed!")
        
        # Demonstrate real-time conversation
        print("\n🎪 Demonstrating Multi-Character Real-Time Conversation...")
        await self.demonstrate_conversation_flow(websocket)
    
    async def demonstrate_conversation_flow(self, websocket):
        """Demonstrate flowing multi-character conversation"""
        
        conversation_flow = [
            {
                'message': 'ARCHITECT, what are your thoughts on building sovereign AI systems?',
                'characters': ['ARCHITECT'],
                'mode': 'single_character'
            },
            {
                'message': 'AIRTH, how would you analyze the data patterns in sovereign AI development?',
                'characters': ['AIRTH'], 
                'mode': 'single_character'
            },
            {
                'message': 'Both of you - how should we integrate philosophical vision with analytical precision?',
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'dual_character'
            }
        ]
        
        print("\n🎭 Multi-Character Conversation Flow")
        print("-" * 40)
        
        for i, turn in enumerate(conversation_flow, 1):
            print(f"\n💬 Turn {i}: {turn['message'][:50]}...")
            
            request = {
                'user_id': f"{self.user_id}_flow",
                'message': turn['message'],
                'characters': turn['characters'],
                'mode': turn['mode']
            }
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get('success'):
                for resp in response_data.get('responses', []):
                    character = resp.get('character')
                    emotion = resp.get('emotion')
                    message = resp.get('message')
                    
                    print(f"🎭 {character} ({emotion}):")
                    print(f"   {message}")
            
            await asyncio.sleep(1.5)
        
        print("\n🎉 Conversation flow demonstration complete!")
    
    def _parse_enhanced_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Parse enhanced command format"""
        parts = command.split(':', 2)
        
        if len(parts) < 2:
            return None
        
        cmd_type = parts[0].lower()
        
        if cmd_type == 'single' and len(parts) == 3:
            character = parts[1].upper()
            message = parts[2]
            return {
                'user_id': 'interactive_user',
                'message': message,
                'characters': [character],
                'mode': 'single_character'
            }
        elif cmd_type == 'dual' and len(parts) == 2:
            message = parts[1]
            return {
                'user_id': 'interactive_user',
                'message': message,
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'dual_character'
            }
        elif cmd_type == 'debate' and len(parts) == 2:
            topic = parts[1]
            return {
                'user_id': 'interactive_user',
                'message': topic,
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'debate'
            }
        elif cmd_type == 'consult' and len(parts) == 2:
            issue = parts[1]
            return {
                'user_id': 'interactive_user',
                'message': issue,
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'consultation'
            }
        
        return None

async def interactive_enhanced_mode():
    """Interactive enhanced conversation mode"""
    client = EnhancedDialogueClient()
    
    def parse_enhanced_command(command: str) -> Optional[Dict[str, Any]]:
        """Parse enhanced command format"""
        parts = command.split(':', 2)
        
        if len(parts) < 2:
            return None
        
        cmd_type = parts[0].lower()
        
        if cmd_type == 'single' and len(parts) == 3:
            character = parts[1].upper()
            message = parts[2]
            return {
                'user_id': 'interactive_user',
                'message': message,
                'characters': [character],
                'mode': 'single_character'
            }
        elif cmd_type == 'dual' and len(parts) == 2:
            message = parts[1]
            return {
                'user_id': 'interactive_user',
                'message': message,
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'dual_character'
            }
        elif cmd_type == 'debate' and len(parts) == 2:
            topic = parts[1]
            return {
                'user_id': 'interactive_user',
                'message': topic,
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'debate'
            }
        elif cmd_type == 'consult' and len(parts) == 2:
            issue = parts[1]
            return {
                'user_id': 'interactive_user',
                'message': issue,
                'characters': ['ARCHITECT', 'AIRTH'],
                'mode': 'consultation'
            }
        
        return None
    
    try:
        async with websockets.connect(client.uri) as websocket:
            print("✅ Connected to Enhanced TEC Dialogue Server")
            print("🎭 Interactive Enhanced Mode")
            print("📝 Commands:")
            print("   single:<character>:<message> - Single character response")
            print("   dual:<message> - Dual character dialogue")
            print("   debate:<topic> - Character debate")
            print("   consult:<issue> - Character consultation")
            print("   quit - Exit")
            
            # Listen for welcome message
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"📡 Available: {', '.join(welcome_data.get('characters', []))}")
            
            while True:
                user_input = input("\n💬 Enhanced Command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Parse enhanced commands
                request = parse_enhanced_command(user_input)
                if not request:
                    print("❌ Invalid command format")
                    continue
                
                await websocket.send(json.dumps(request))
                response = await websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get('success'):
                    responses = response_data.get('responses', [])
                    mode = response_data.get('mode')
                    
                    print(f"\n🎪 {mode.replace('_', ' ').title()} Response:")
                    for resp in responses:
                        character = resp.get('character')
                        emotion = resp.get('emotion')
                        message = resp.get('message')
                        
                        print(f"🎭 {character} ({emotion}):")
                        print(f"   {message}")
                else:
                    error_msg = response_data.get('message', 'Unknown error')
                    print(f"❌ Error: {error_msg}")
    
    except websockets.exceptions.ConnectionRefused:
        print("❌ Cannot connect. Is the enhanced server running on localhost:8766?")
    except KeyboardInterrupt:
        print("\n👋 Enhanced session ended!")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main entry point"""
    print("🎭 Enhanced TEC Dialogue System Test Client")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        print("🎮 Starting enhanced interactive mode...")
        asyncio.run(interactive_enhanced_mode())
    else:
        print("🧪 Running enhanced automated test scenarios...")
        client = EnhancedDialogueClient()
        asyncio.run(client.connect_and_test())

if __name__ == "__main__":
    main()
