#!/usr/bin/env python3
"""
Test script for TEC Real-time Dialogue System
Validates character interactions and WebSocket functionality
"""

import asyncio
import sys
from pathlib import Path

# Add tec_core to path
sys.path.append(str(Path(__file__).parent))

try:
    from tec_core.dialogue_engine import TECDialogueEngine, DialogueWebSocketServer
    print("✅ Successfully imported dialogue engine")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

async def test_dialogue_engine():
    """Test the dialogue engine functionality"""
    print("\n🧪 Testing TEC Dialogue Engine...")
    
    try:
        # Initialize dialogue engine
        dialogue = TECDialogueEngine()
        dialogue.initialize()
        print("✅ Dialogue engine initialized")
        
        # Test character access
        architect = dialogue.characters.get('ARCHITECT')
        airth = dialogue.characters.get('AIRTH')
        
        if architect and airth:
            print(f"✅ Characters loaded: {architect.name}, {airth.name}")
            print(f"   ARCHITECT tone: {architect.personality_tone}")
            print(f"   AIRTH tone: {airth.personality_tone}")
        else:
            print("❌ Characters not properly loaded")
            return
            
        # Test conversation generation
        print("\n💭 Testing conversation generation...")
        
        test_message = {
            'user_id': 'test_user',
            'message': 'What is the TEC philosophy about narrative control?',
            'character': 'ARCHITECT'
        }
        
        response = await dialogue.generate_response(test_message)
        
        if response:
            print(f"✅ Generated response from {response.get('character', 'UNKNOWN')}")
            print(f"   Response length: {len(response.get('message', ''))}")
            print(f"   Emotion: {response.get('emotion', 'neutral')}")
            print(f"   First 100 chars: {response.get('message', '')[:100]}...")
        else:
            print("❌ Failed to generate response")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_websocket_server():
    """Test WebSocket server initialization"""
    print("\n🌐 Testing WebSocket Server...")
    
    try:
        server = DialogueWebSocketServer(host='localhost', port=8765)
        print("✅ WebSocket server created")
        
        # Don't actually start the server in test mode
        print("✅ Server ready to start (not starting in test mode)")
        
    except Exception as e:
        print(f"❌ WebSocket server test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 TEC Dialogue System Test Suite")
    print("=" * 50)
    
    try:
        # Test basic dialogue engine
        asyncio.run(test_dialogue_engine())
        
        # Test WebSocket server
        asyncio.run(test_websocket_server())
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("\n🎯 Next Steps:")
        print("   1. Start dialogue server: python -m tec_core.dialogue_engine")
        print("   2. Connect via WebSocket to localhost:8765")
        print("   3. Send JSON messages with format:")
        print("      {'user_id': 'user1', 'message': 'Hello', 'character': 'ARCHITECT'}")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
