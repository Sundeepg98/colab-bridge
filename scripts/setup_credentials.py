#!/usr/bin/env python3
"""
Interactive setup for Claude Tools credentials
"""

import os
import json
import sys
from pathlib import Path

def setup_credentials():
    """Interactive credential setup"""
    print("🔐 Claude Tools Credential Setup")
    print("================================\n")
    
    root = Path(__file__).parent.parent
    env_file = root / ".env"
    
    # Check if .env already exists
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Setup cancelled")
            return
    
    print("\n📋 We need the following:")
    print("1. Path to your Google service account JSON file")
    print("2. Google Drive folder ID for commands/results")
    print("3. (Optional) API keys for AI services\n")
    
    # Get service account path
    while True:
        sa_path = input("Enter path to service account JSON file: ").strip()
        if sa_path.startswith('"') and sa_path.endswith('"'):
            sa_path = sa_path[1:-1]  # Remove quotes
        
        if not sa_path:
            print("❌ Path cannot be empty")
            continue
            
        sa_path = Path(sa_path).expanduser().absolute()
        
        if not sa_path.exists():
            print(f"❌ File not found: {sa_path}")
            continue
            
        try:
            # Validate it's a valid service account file
            with open(sa_path) as f:
                data = json.load(f)
                if 'type' in data and data['type'] == 'service_account':
                    print("✅ Valid service account file")
                    break
                else:
                    print("❌ Not a valid service account JSON file")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    # Get Drive folder ID
    print("\n📁 Google Drive Folder Setup")
    print("1. Create a folder in Google Drive")
    print("2. Share it with your service account email")
    print("3. Copy the folder ID from the URL")
    print("   Example URL: https://drive.google.com/drive/folders/[FOLDER_ID_HERE]")
    
    while True:
        folder_id = input("\nEnter Google Drive folder ID: ").strip()
        if not folder_id:
            print("❌ Folder ID cannot be empty")
            continue
        if len(folder_id) > 20:  # Basic validation
            print("✅ Folder ID saved")
            break
        else:
            print("❌ Invalid folder ID")
    
    # Optional API keys
    print("\n🔑 Optional API Keys (press Enter to skip)")
    anthropic_key = input("Anthropic API Key (for Claude): ").strip()
    openai_key = input("OpenAI API Key (for GPT): ").strip()
    
    # Create .env file
    env_content = f"""# Claude Tools Configuration
# Generated by setup_credentials.py

# Google Service Account (for Drive API access)
SERVICE_ACCOUNT_PATH={sa_path}
GOOGLE_DRIVE_FOLDER_ID={folder_id}

# AI API Keys (optional but recommended)
ANTHROPIC_API_KEY={anthropic_key}
OPENAI_API_KEY={openai_key}

# Security
SECRET_KEY=your-secret-key-here

# Development settings
DEBUG=false
LOG_LEVEL=INFO
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("\n✅ Configuration saved to .env")
    
    # Test the configuration
    print("\n🧪 Testing configuration...")
    
    # Add parent to path
    sys.path.insert(0, str(root))
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from colab_integration.bridge import ClaudeColabBridge
        
        bridge = ClaudeColabBridge()
        bridge.initialize()
        
        print("✅ Google Drive connection successful!")
        print("\n🎉 Setup complete! You can now use Claude Tools")
        print("\n📝 Next steps:")
        print("1. Open a Colab notebook from notebooks/ folder")
        print("2. Run the notebook to start the processor")
        print("3. Test with: python scripts/test_basic.py")
        
    except Exception as e:
        print(f"\n❌ Configuration test failed: {e}")
        print("\nPlease check:")
        print("1. Service account has access to the Drive folder")
        print("2. Drive API is enabled in Google Cloud Console")
        print("3. All paths and IDs are correct")

if __name__ == "__main__":
    setup_credentials()