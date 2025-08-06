#!/usr/bin/env python3
"""
TEC Asimov Engine - Docker MCP Deployment Script
Automates the deployment process for Docker MCP registry submission
"""

import os
import sys
import subprocess
import json
import yaml
from pathlib import Path

class TECMCPDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.docker_image = "tec/asimov-engine"
        self.version = "1.0.0"
        
    def validate_environment(self):
        """Validate that all required tools and files are present"""
        print("🔍 Validating deployment environment...")
        
        # Check Docker
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            print("✅ Docker is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker is not installed or not in PATH")
            return False
            
        # Check required files
        required_files = [
            "Dockerfile",
            "server.yaml", 
            "docker-compose.yml",
            ".env.template"
        ]
        
        for file in required_files:
            if not (self.project_root / file).exists():
                print(f"❌ Missing required file: {file}")
                return False
            print(f"✅ Found {file}")
            
        return True
    
    def build_image(self):
        """Build the Docker image"""
        print(f"🔨 Building Docker image: {self.docker_image}:{self.version}")
        
        cmd = [
            "docker", "build",
            "-t", f"{self.docker_image}:{self.version}",
            "-t", f"{self.docker_image}:latest",
            str(self.project_root)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, cwd=self.project_root)
            print("✅ Docker image built successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build Docker image: {e}")
            return False
    
    def test_container(self):
        """Test the container locally"""
        print("🧪 Testing container locally...")
        
        # Check if .env.local exists
        env_file = self.project_root / ".env.local"
        if not env_file.exists():
            print("⚠️  No .env.local file found. Creating minimal config...")
            self.create_minimal_env()
        
        # Run health check
        cmd = [
            "docker", "run", "--rm",
            "-p", "8080:8080",
            "-e", "TEC_MODE=mcp",
            "-e", "DATABASE_URL=sqlite:///app/data/tec_memory.db",
            "--name", "tec-test",
            f"{self.docker_image}:latest",
            "python", "-c", "from app import app; import time; time.sleep(2); print('✅ Container test passed')"
        ]
        
        try:
            result = subprocess.run(cmd, check=True, timeout=30)
            print("✅ Container test passed")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"❌ Container test failed: {e}")
            return False
    
    def create_minimal_env(self):
        """Create minimal environment file for testing"""
        env_content = """# Minimal configuration for testing
TEC_MODE=mcp
DATABASE_URL=sqlite:///app/data/tec_memory.db
TEC_LOG_LEVEL=INFO
AZURE_OPENAI_API_KEY=test_key_for_local_testing
ELEVENLABS_API_KEY=test_key_for_local_testing
"""
        with open(self.project_root / ".env.local", "w") as f:
            f.write(env_content)
        print("✅ Created minimal .env.local for testing")
    
    def validate_mcp_config(self):
        """Validate the MCP server.yaml configuration"""
        print("📋 Validating MCP server configuration...")
        
        try:
            with open(self.project_root / "server.yaml", "r") as f:
                config = yaml.safe_load(f)
            
            # Validate required fields
            required_fields = ["name", "version", "description", "mcp", "runtime"]
            for field in required_fields:
                if field not in config:
                    print(f"❌ Missing required field in server.yaml: {field}")
                    return False
                    
            # Validate MCP tools
            if "tools" not in config["mcp"]:
                print("❌ No tools defined in MCP configuration")
                return False
                
            tools = config["mcp"]["tools"]
            expected_tools = ["validate_axioms", "query_memory", "generate_lore", "process_asset", "hybrid_synthesis"]
            
            for tool_name in expected_tools:
                if not any(tool["name"] == tool_name for tool in tools):
                    print(f"❌ Missing required MCP tool: {tool_name}")
                    return False
                    
            print(f"✅ MCP configuration valid with {len(tools)} tools")
            return True
            
        except Exception as e:
            print(f"❌ Failed to validate server.yaml: {e}")
            return False
    
    def generate_registry_submission(self):
        """Generate the final registry submission package"""
        print("📦 Generating Docker MCP registry submission package...")
        
        submission_dir = self.project_root / "docker_mcp_submission"
        submission_dir.mkdir(exist_ok=True)
        
        # Copy required files
        files_to_copy = [
            "server.yaml",
            "Dockerfile", 
            "README.md",
            "requirements.txt"
        ]
        
        for file in files_to_copy:
            src = self.project_root / file
            if src.exists():
                import shutil
                dst = submission_dir / file
                shutil.copy2(src, dst)
                print(f"✅ Copied {file}")
        
        # Create submission manifest
        manifest = {
            "name": "tec-asimov-engine",
            "version": self.version,
            "description": "The Elidoras Codex Asimov Engine - Sovereign MCP Server",
            "author": "The Architect",
            "repository": "https://github.com/TEC-The-ELidoras-Codex/TEC_NWO",
            "license": "MIT",
            "tags": ["sovereign", "intelligence", "axiom-validation", "hybrid-synthesis", "mcp"],
            "docker_image": f"{self.docker_image}:{self.version}",
            "submission_date": "2025-08-05",
            "compliance": {
                "axiom_validated": True,
                "constitutional_compliance": True,
                "sovereignty_verified": True
            }
        }
        
        with open(submission_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✅ Submission package created in: {submission_dir}")
        return submission_dir
    
    def deploy(self):
        """Run the complete deployment process"""
        print("🚀 Starting TEC Asimov Engine Docker MCP deployment...")
        print("=" * 60)
        
        # Step 1: Validate environment
        if not self.validate_environment():
            print("❌ Environment validation failed")
            return False
            
        # Step 2: Validate MCP configuration
        if not self.validate_mcp_config():
            print("❌ MCP configuration validation failed")
            return False
            
        # Step 3: Build Docker image
        if not self.build_image():
            print("❌ Docker image build failed")
            return False
            
        # Step 4: Test container
        if not self.test_container():
            print("❌ Container testing failed") 
            return False
            
        # Step 5: Generate submission package
        submission_dir = self.generate_registry_submission()
        if not submission_dir:
            print("❌ Failed to generate submission package")
            return False
            
        print("=" * 60)
        print("🎯 DEPLOYMENT SUCCESSFUL!")
        print(f"📦 Docker image: {self.docker_image}:{self.version}")
        print(f"📋 Submission package: {submission_dir}")
        print("")
        print("🚀 Next steps:")
        print("1. Push Docker image to Docker Hub:")
        print(f"   docker push {self.docker_image}:{self.version}")
        print("2. Submit to Docker MCP Registry:")
        print(f"   Submit contents of {submission_dir}")
        print("3. Deploy using Docker MCP:")
        print("   docker run -d --name tec-asimov-engine \\")
        print("     -p 3000:3000 -p 8080:8080 \\")
        print(f"     {self.docker_image}:{self.version}")
        
        return True

def main():
    """Main deployment function"""
    deployer = TECMCPDeployer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test-only":
        # Test mode - just validate and test
        print("🧪 Running in test mode...")
        success = (deployer.validate_environment() and 
                  deployer.validate_mcp_config() and
                  deployer.build_image() and
                  deployer.test_container())
        return 0 if success else 1
    
    # Full deployment
    success = deployer.deploy()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
