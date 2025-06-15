#!/usr/bin/env python3
"""
Claude Tools Setup Script
Quick setup for new installations
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    """Main setup process"""
    print("🚀 Claude Tools Setup")
    print("====================")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print("✅ Python version OK")
    
    # Check if .env exists
    env_file = Path(".env")
    env_template = Path("config/.env.template")
    
    if not env_file.exists() and env_template.exists():
        print("📄 Creating .env from template...")
        shutil.copy(env_template, env_file)
        print("✅ .env created - please edit with your credentials")
    else:
        print("✅ .env file exists")
    
    # Install dependencies
    print("📦 Installing dependencies...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    # Create necessary directories
    dirs = ["temp", "logs"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    print("✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .env with your API keys and credentials")
    print("2. Add your Google service account JSON file")
    print("3. Test with: python scripts/test_basic.py")

if __name__ == "__main__":
    main()