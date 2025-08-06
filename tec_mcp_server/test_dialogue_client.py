#!/usr/bin/env python3
"""
TEC Dialogue System Test Client
Interactive WebSocket client for testing character conversations
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime

class DialogueClient:
    """Test client for TEC dialogue system"""
    
    def __init__(self, uri='ws://localhost:8765'):
        self.uri = uri
        self.user_id = 'test_user'
        
    async def connect_and_test(self):
        """Connect to server and run interactive tests"""
        try:
            async with websockets.connect(self.uri) as websocket:
                print("✅ Connected to TEC Dialogue Server")
                
                # Listen for welcome message
                welcome = await websocket.recv()
                welcome_data = json.loads(welcome)
                print(f"📡 {welcome_data.get('message')}")
                print(f"🎭 Available characters: {', '.join(welcome_data.get('characters', []))}")
                
                # Run test conversations
                await self.run_test_scenarios(websocket)
                
        except websockets.exceptions.ConnectionRefused:
            print("❌ Cannot connect to dialogue server. Is it running on localhost:8765?")
        except Exception as e:
            print(f"❌ Connection error: {e}")
    
    async def run_test_scenarios(self, websocket):
        """Run automated test scenarios"""
        test_scenarios = [
            {
                'character': 'ARCHITECT',
                'message': 'What is the TEC philosophy about narrative control?',
                'expected_themes': ['narrative', 'sovereignty', 'blueprint']
            },
            {
                'character': 'AIRTH', 
                'message': 'How do you analyze emotional data patterns?',
                'expected_themes': ['patterns', 'analysis', 'data']
            },
            {
                'character': 'ARCHITECT',
                'message': 'Tell me about building for future generations',
                'expected_themes': ['generations', 'foundation', 'responsibility']
            }
        ]
        
        print("\n🧪 Running Test Scenarios")
        print("=" * 50)
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n🎯 Test {i}: {scenario['character']} - {scenario['message'][:50]}...")
            
            # Send message
            request = {
                'user_id': self.user_id,
                'message': scenario['message'],
                'character': scenario['character']
            }
            
            await websocket.send(json.dumps(request))
            
            # Wait for response
            response = await websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get('type') == 'character_response':
                character = response_data.get('character')
                message = response_data.get('message')
                emotion = response_data.get('emotion')
                
                print(f"✅ {character} ({emotion}): {message[:100]}...")
                
                # Check for expected themes
                themes_found = [theme for theme in scenario['expected_themes'] 
                              if theme.lower() in message.lower()]
                if themes_found:
                    print(f"🎯 Themes detected: {', '.join(themes_found)}")
                else:
                    print("⚠️  Expected themes not found in response")
            else:
                print(f"❌ Unexpected response: {response_data}")
            
            await asyncio.sleep(1)  # Brief pause between tests
        
        print("\n" + "=" * 50)
        print("✅ All test scenarios completed!")

async def interactive_mode():
    """Interactive conversation mode"""
    client = DialogueClient()
    
    try:
        async with websockets.connect(client.uri) as websocket:
            print("✅ Connected to TEC Dialogue Server")
            print("🎭 Interactive mode - type 'quit' to exit")
            print("📝 Format: <character>: <message> (e.g., 'ARCHITECT: Hello')")
            
            # Listen for welcome message
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"📡 Available characters: {', '.join(welcome_data.get('characters', []))}")
            
            while True:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Parse input
                if ':' in user_input:
                    character, message = user_input.split(':', 1)
                    character = character.strip().upper()
                    message = message.strip()
                else:
                    character = 'ARCHITECT'
                    message = user_input
                
                # Send request
                request = {
                    'user_id': 'interactive_user',
                    'message': message,
                    'character': character
                }
                
                await websocket.send(json.dumps(request))
                
                # Wait for response
                response = await websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get('type') == 'character_response':
                    char_name = response_data.get('character')
                    char_message = response_data.get('message')
                    emotion = response_data.get('emotion')
                    
                    print(f"🎭 {char_name} ({emotion}):")
                    print(f"   {char_message}")
                else:
                    print(f"❌ Error: {response_data.get('message', 'Unknown error')}")
    
    except websockets.exceptions.ConnectionRefused:
        print("❌ Cannot connect to dialogue server. Is it running on localhost:8765?")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main entry point"""
    print("🎭 TEC Dialogue System Test Client")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        print("🎮 Starting interactive mode...")
        asyncio.run(interactive_mode())
    else:
        print("🧪 Running automated test scenarios...")
        client = DialogueClient()
        asyncio.run(client.connect_and_test())

if __name__ == "__main__":
    main()
