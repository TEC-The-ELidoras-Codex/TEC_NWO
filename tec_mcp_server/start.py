#!/usr/bin/env python3
"""
TEC MCP Server Startup Script
Quick development setup and launch
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if environment is properly configured"""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from template...")
        template_file = Path('.env.template')
        if template_file.exists():
            subprocess.run(['cp', '.env.template', '.env'])
            print("✅ .env file created. Please edit it with your configuration.")
            return False
        else:
            print("❌ .env.template not found. Cannot create environment file.")
            return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_server():
    """Start the Asimov Engine server"""
    print("🏛️  Starting TEC MCP Server - The Asimov Engine...")
    print("🚀 Server will be available at http://localhost:5000")
    print("📊 Health check: http://localhost:5000/health")
    print()
    
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")

def main():
    """Main startup sequence"""
    print("🏛️  TEC MCP SERVER - THE ASIMOV ENGINE")
    print("Genesis Version: 071225_001")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Please configure your .env file and run again.")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start server
    start_server()

if __name__ == '__main__':
    main()
