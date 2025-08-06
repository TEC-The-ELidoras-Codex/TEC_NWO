#!/usr/bin/env python3
"""
TEC Asimov Engine - Docker Secrets Management
Secure handling of API keys and sensitive configuration for Docker MCP deployment
"""

import os
import sys
import json
import base64
import subprocess
from pathlib import Path
from cryptography.fernet import Fernet
from getpass import getpass

class TECSecretsManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.secrets_dir = self.project_root / ".secrets"
        self.secrets_dir.mkdir(exist_ok=True, mode=0o700)
        
        # Master key file
        self.key_file = self.secrets_dir / "master.key"
        self.secrets_file = self.secrets_dir / "secrets.enc"
        
    def generate_master_key(self):
        """Generate a new master encryption key"""
        if self.key_file.exists():
            response = input("Master key already exists. Regenerate? (y/N): ")
            if response.lower() != 'y':
                return False
                
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as f:
            f.write(key)
        os.chmod(self.key_file, 0o600)
        print("✅ Master encryption key generated")
        return True
        
    def load_master_key(self):
        """Load the master encryption key"""
        if not self.key_file.exists():
            print("❌ Master key not found. Run: python secrets_manager.py --generate-key")
            return None
            
        with open(self.key_file, "rb") as f:
            return f.read()
            
    def encrypt_secrets(self, secrets_dict):
        """Encrypt secrets dictionary"""
        key = self.load_master_key()
        if not key:
            return False
            
        fernet = Fernet(key)
        secrets_json = json.dumps(secrets_dict, indent=2)
        encrypted_data = fernet.encrypt(secrets_json.encode())
        
        with open(self.secrets_file, "wb") as f:
            f.write(encrypted_data)
        os.chmod(self.secrets_file, 0o600)
        
        print("✅ Secrets encrypted and stored")
        return True
        
    def decrypt_secrets(self):
        """Decrypt and return secrets dictionary"""
        key = self.load_master_key()
        if not key:
            return None
            
        if not self.secrets_file.exists():
            print("❌ Encrypted secrets file not found")
            return None
            
        fernet = Fernet(key)
        
        with open(self.secrets_file, "rb") as f:
            encrypted_data = f.read()
            
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"❌ Failed to decrypt secrets: {e}")
            return None
    
    def collect_secrets_interactive(self):
        """Interactively collect secrets from user"""
        print("🔐 TEC Asimov Engine - Secrets Collection")
        print("=" * 50)
        print("Enter your API keys and sensitive configuration.")
        print("These will be encrypted and stored securely.")
        print("")
        
        secrets = {}
        
        # Azure OpenAI
        print("Azure OpenAI Configuration:")
        secrets["AZURE_OPENAI_API_KEY"] = getpass("Azure OpenAI API Key: ")
        secrets["AZURE_OPENAI_ENDPOINT"] = input("Azure OpenAI Endpoint: ")
        secrets["AZURE_OPENAI_DEPLOYMENT"] = input("Azure OpenAI Deployment (default: gpt-4): ") or "gpt-4"
        
        print("")
        
        # ElevenLabs
        print("ElevenLabs Configuration:")
        secrets["ELEVENLABS_API_KEY"] = getpass("ElevenLabs API Key: ")
        
        print("")
        
        # Database
        print("Database Configuration:")
        db_choice = input("Database type (sqlite/postgresql) [sqlite]: ").lower() or "sqlite"
        
        if db_choice == "postgresql":
            secrets["DATABASE_URL"] = input("PostgreSQL URL: ")
        else:
            secrets["DATABASE_URL"] = "sqlite:///app/data/tec_memory.db"
            
        print("")
        
        # Security
        print("Security Configuration:")
        jwt_secret = input("JWT Secret (leave empty to generate): ")
        if not jwt_secret:
            import secrets as crypto_secrets
            jwt_secret = crypto_secrets.token_urlsafe(32)
            print(f"Generated JWT Secret: {jwt_secret}")
        secrets["JWT_SECRET_KEY"] = jwt_secret
        
        print("")
        
        # Optional Redis
        redis_url = input("Redis URL (optional): ")
        if redis_url:
            secrets["REDIS_URL"] = redis_url
            
        return secrets
    
    def create_docker_secrets(self, secrets_dict):
        """Create Docker secrets from encrypted secrets"""
        print("🐳 Creating Docker secrets...")
        
        for key, value in secrets_dict.items():
            secret_name = f"tec.{key.lower()}"
            
            try:
                # Create Docker secret
                cmd = ["docker", "secret", "create", secret_name, "-"]
                result = subprocess.run(
                    cmd,
                    input=value.encode(),
                    check=True,
                    capture_output=True
                )
                print(f"✅ Created Docker secret: {secret_name}")
                
            except subprocess.CalledProcessError as e:
                if "already exists" in e.stderr.decode():
                    print(f"⚠️  Docker secret already exists: {secret_name}")
                else:
                    print(f"❌ Failed to create Docker secret {secret_name}: {e}")
                    
    def export_env_file(self, output_file=".env.local"):
        """Export decrypted secrets to environment file"""
        secrets = self.decrypt_secrets()
        if not secrets:
            return False
            
        env_path = self.project_root / output_file
        
        with open(env_path, "w") as f:
            f.write("# TEC Asimov Engine - Environment Configuration\n")
            f.write("# Generated from encrypted secrets store\n")
            f.write(f"# Generated: {__import__('datetime').datetime.now()}\n\n")
            
            # MCP Configuration
            f.write("# === MCP SERVER CONFIGURATION ===\n")
            f.write("TEC_MODE=mcp\n")
            f.write("PYTHONPATH=/app\n")
            f.write("TEC_LOG_LEVEL=INFO\n\n")
            
            # Secrets
            f.write("# === SECRETS ===\n")
            for key, value in secrets.items():
                f.write(f"{key}={value}\n")
                
            f.write("\n# === SOVEREIGNTY CONFIGURATION ===\n")
            f.write("AXIOM_VALIDATION_THRESHOLD=0.8\n")
            f.write("HYBRID_ANALOG_INFLUENCE=0.7\n")
            f.write("MEMORY_SEARCH_THRESHOLD=0.75\n")
        
        os.chmod(env_path, 0o600)
        print(f"✅ Environment file exported: {env_path}")
        return True
    
    def validate_secrets(self):
        """Validate that all required secrets are present"""
        secrets = self.decrypt_secrets()
        if not secrets:
            return False
            
        required_secrets = [
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_ENDPOINT", 
            "ELEVENLABS_API_KEY",
            "DATABASE_URL",
            "JWT_SECRET_KEY"
        ]
        
        missing = []
        for secret in required_secrets:
            if secret not in secrets or not secrets[secret]:
                missing.append(secret)
                
        if missing:
            print(f"❌ Missing required secrets: {', '.join(missing)}")
            return False
            
        print("✅ All required secrets present")
        return True

def main():
    """Main secrets management function"""
    manager = TECSecretsManager()
    
    if len(sys.argv) < 2:
        print("TEC Asimov Engine - Secrets Manager")
        print("")
        print("Usage:")
        print("  python secrets_manager.py --generate-key")
        print("  python secrets_manager.py --collect")
        print("  python secrets_manager.py --export")
        print("  python secrets_manager.py --create-docker-secrets")
        print("  python secrets_manager.py --validate")
        return 1
        
    command = sys.argv[1]
    
    if command == "--generate-key":
        manager.generate_master_key()
        
    elif command == "--collect":
        if not manager.key_file.exists():
            print("Generating master key first...")
            manager.generate_master_key()
            
        secrets = manager.collect_secrets_interactive()
        manager.encrypt_secrets(secrets)
        print("")
        print("✅ Secrets collected and encrypted")
        print("Next steps:")
        print("  python secrets_manager.py --export")
        print("  python secrets_manager.py --validate")
        
    elif command == "--export":
        output_file = sys.argv[2] if len(sys.argv) > 2 else ".env.local"
        manager.export_env_file(output_file)
        
    elif command == "--create-docker-secrets":
        secrets = manager.decrypt_secrets()
        if secrets:
            manager.create_docker_secrets(secrets)
        else:
            print("❌ No secrets found. Run --collect first.")
            
    elif command == "--validate":
        manager.validate_secrets()
        
    else:
        print(f"❌ Unknown command: {command}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
