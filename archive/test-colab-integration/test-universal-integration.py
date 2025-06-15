#!/usr/bin/env python3
"""
Test the Universal Colab Integration
Demonstrates how any project can use it
"""

import json
import os
import sys
from datetime import datetime

# Add path to access Google API
sys.path.append('/var/projects/movie-booking-app/backend')

try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
except ImportError:
    print("❌ Google API libraries not available in this environment")
    print("This would work in a proper Python environment with google-api-python-client installed")
    exit(1)

# Configuration
SERVICE_ACCOUNT_FILE = '/var/projects/eng-flux-459812-q6-e05c54813553.json'
COLAB_FOLDER_ID = '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z'  # From previous setup

def test_integration():
    """Test sending commands to Colab via the universal integration"""
    
    print("🧪 Testing Universal Colab Integration")
    print("=====================================\n")
    
    # Load service account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # Build Drive service
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # Test commands to send
    test_commands = [
        {
            "id": f"test_simple_{int(datetime.now().timestamp())}",
            "type": "execute_code",
            "code": "print('Hello from test project!')\nprint(2 + 2)",
            "project": "test_integration"
        },
        {
            "id": f"test_install_{int(datetime.now().timestamp())}",
            "type": "install_package",
            "package": "requests",
            "project": "test_integration"
        },
        {
            "id": f"test_analysis_{int(datetime.now().timestamp())}",
            "type": "data_analysis",
            "data": {
                "values": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            },
            "project": "test_integration"
        }
    ]
    
    print("📤 Sending test commands to Colab...\n")
    
    for cmd in test_commands:
        try:
            # Create command file
            file_metadata = {
                'name': f'command_{cmd["id"]}.json',
                'parents': [COLAB_FOLDER_ID],
                'mimeType': 'application/json'
            }
            
            # Upload command
            from googleapiclient.http import MediaInMemoryUpload
            media = MediaInMemoryUpload(
                json.dumps(cmd, indent=2).encode('utf-8'),
                mimetype='application/json'
            )
            
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name'
            ).execute()
            
            print(f"✅ Sent: {cmd['type']} (ID: {cmd['id']})")
            print(f"   File: {file['name']}")
            
        except Exception as e:
            print(f"❌ Error sending {cmd['type']}: {e}")
    
    print("\n📊 Summary:")
    print(f"Commands sent: {len(test_commands)}")
    print(f"Location: ColabAPI folder (ID: {COLAB_FOLDER_ID})")
    
    print("\n🎯 To process these commands:")
    print("1. Open Google Colab")
    print("2. Paste UNIVERSAL_COLAB_CLAUDE_INTEGRATION.py")
    print(f"3. Set PROJECT_NAME = 'test_integration'")
    print(f"4. Set SERVICE_ACCOUNT_FOLDER_ID = '{COLAB_FOLDER_ID}'")
    print("5. Run the cell")
    print("\n✨ The commands will be processed automatically!")

if __name__ == "__main__":
    test_integration()