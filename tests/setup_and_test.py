#!/usr/bin/env python3
"""
Setup and test colab-bridge functionality
"""

import os
import sys
import json
import time
from pathlib import Path

# Add colab_integration to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up environment
os.environ['SERVICE_ACCOUNT_PATH'] = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
os.environ['SERVICE_ACCOUNT_KEY_PATH'] = os.environ['SERVICE_ACCOUNT_PATH']
os.environ['OWNER_EMAIL'] = 'sundeepg8@gmail.com'

print("🚀 COLAB-BRIDGE SETUP AND TEST")
print("=" * 60)

# Step 1: Create a dedicated folder for colab-bridge
print("\n1️⃣ Creating dedicated folder for colab-bridge...")

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    
    # Initialize Drive service
    credentials = service_account.Credentials.from_service_account_file(
        os.environ['SERVICE_ACCOUNT_PATH'],
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # Create folder
    folder_metadata = {
        'name': f'colab-bridge-integration-{int(time.time())}',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    folder = drive_service.files().create(
        body=folder_metadata,
        fields='id,name,webViewLink'
    ).execute()
    
    folder_id = folder['id']
    print(f"✅ Created folder: {folder['name']}")
    print(f"   ID: {folder_id}")
    print(f"   URL: {folder.get('webViewLink', 'N/A')}")
    
    # Share with owner
    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': os.environ['OWNER_EMAIL']
    }
    
    drive_service.permissions().create(
        fileId=folder_id,
        body=permission,
        sendNotificationEmail=False
    ).execute()
    
    print(f"✅ Shared with: {os.environ['OWNER_EMAIL']}")
    
    # Update environment
    os.environ['GOOGLE_DRIVE_FOLDER_ID'] = folder_id
    
except Exception as e:
    print(f"❌ Error creating folder: {e}")
    sys.exit(1)

# Step 2: Create a test notebook
print("\n2️⃣ Creating test notebook...")

try:
    # Create the processor notebook
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Colab-Bridge Processor\\n", "Auto-processing commands from colab-bridge"]
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [
                    "import json\\n",
                    "import time\\n",
                    "from google.colab import drive\\n",
                    "drive.mount('/content/drive')\\n",
                    "print('✅ Drive mounted')"
                ]
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": [
                    "# Processor loop\\n",
                    "folder_path = f'/content/drive/MyDrive/{folder['name']}'\\n",
                    "print(f'📁 Monitoring: {folder_path}')\\n",
                    "\\n",
                    "while True:\\n",
                    "    # Check for command files\\n",
                    "    import os\\n",
                    "    if os.path.exists(folder_path):\\n",
                    "        for file in os.listdir(folder_path):\\n",
                    "            if file.startswith('command_') and file.endswith('.json'):\\n",
                    "                # Process command\\n",
                    "                cmd_path = os.path.join(folder_path, file)\\n",
                    "                with open(cmd_path, 'r') as f:\\n",
                    "                    command = json.load(f)\\n",
                    "                \\n",
                    "                print(f'⚡ Processing: {command[\"id\"]}')\\n",
                    "                \\n",
                    "                # Execute code\\n",
                    "                result = {'id': command['id'], 'status': 'success'}\\n",
                    "                try:\\n",
                    "                    exec_globals = {}\\n",
                    "                    exec(command['code'], exec_globals)\\n",
                    "                    result['output'] = 'Code executed successfully'\\n",
                    "                except Exception as e:\\n",
                    "                    result['status'] = 'error'\\n",
                    "                    result['error'] = str(e)\\n",
                    "                \\n",
                    "                # Write result\\n",
                    "                result_path = cmd_path.replace('command_', 'result_')\\n",
                    "                with open(result_path, 'w') as f:\\n",
                    "                    json.dump(result, f)\\n",
                    "                \\n",
                    "                # Delete command file\\n",
                    "                os.remove(cmd_path)\\n",
                    "                print(f'✅ Completed: {command[\"id\"]}')\\n",
                    "    \\n",
                    "    time.sleep(2)  # Check every 2 seconds"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    
    # Save notebook locally first
    notebook_path = Path(__file__).parent / 'test_processor.ipynb'
    with open(notebook_path, 'w') as f:
        json.dump(notebook_content, f, indent=2)
    
    print(f"✅ Created notebook: {notebook_path}")
    
    # Upload to Drive
    from googleapiclient.http import MediaFileUpload
    
    file_metadata = {
        'name': 'colab_bridge_processor.ipynb',
        'parents': [folder_id],
        'mimeType': 'application/vnd.google.colab'
    }
    
    media = MediaFileUpload(
        str(notebook_path),
        mimetype='application/vnd.google.colab',
        resumable=True
    )
    
    notebook_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id,name,webViewLink'
    ).execute()
    
    print(f"✅ Uploaded notebook to Drive")
    print(f"   ID: {notebook_file['id']}")
    print(f"   URL: https://colab.research.google.com/drive/{notebook_file['id']}")
    
except Exception as e:
    print(f"❌ Error creating notebook: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Test the bridge
print("\n3️⃣ Testing colab-bridge...")

try:
    from colab_integration.universal_bridge import UniversalColabBridge
    
    # Create .env file
    env_content = f"""SERVICE_ACCOUNT_PATH={os.environ['SERVICE_ACCOUNT_PATH']}
GOOGLE_DRIVE_FOLDER_ID={folder_id}
OWNER_EMAIL={os.environ['OWNER_EMAIL']}
"""
    
    env_path = Path(__file__).parent / '.env'
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created .env file")
    
    # Initialize bridge
    bridge = UniversalColabBridge("test")
    bridge.initialize()
    
    print("✅ Bridge initialized")
    
    # Test code execution
    print("\n📤 Sending test code...")
    test_code = '''
import sys
print(f"Python version: {sys.version}")
print("Hello from Colab!")
'''
    
    result = bridge.execute_code(test_code, timeout=10)
    print(f"📥 Result: {result}")
    
except Exception as e:
    print(f"❌ Error testing bridge: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("📋 SUMMARY")
print("=" * 60)
print(f"✅ Folder created: {folder_id}")
print(f"✅ Notebook created: {notebook_file['id']}")
print(f"✅ Environment configured")
print("\n🎯 Next Steps:")
print(f"1. Open the notebook: https://colab.research.google.com/drive/{notebook_file['id']}")
print(f"2. Run all cells in the notebook")
print(f"3. Come back and run: python3 test_now.py")
print("\n💡 The notebook will process commands automatically!")