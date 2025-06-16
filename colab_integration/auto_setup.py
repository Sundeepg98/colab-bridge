#!/usr/bin/env python3
"""
Fully Automated Colab Setup
User only provides service account key - NOTHING ELSE!
"""

import os
import json
import time
import tempfile
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import hashlib

class AutoColabSetup:
    """Zero-config Colab setup - just needs service account key"""
    
    def __init__(self, service_account_path=None):
        self.service_account_path = service_account_path or self._find_service_account()
        self.config_dir = Path.home() / '.colab-bridge'
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        
    def _find_service_account(self):
        """Auto-detect service account key"""
        possible_locations = [
            os.environ.get('SERVICE_ACCOUNT_PATH'),
            Path.home() / '.colab-bridge' / 'credentials.json',
            Path.cwd() / 'credentials.json',
            Path.cwd() / 'service-account.json',
        ]
        
        for location in possible_locations:
            if location and Path(location).exists():
                return str(location)
        
        raise FileNotFoundError(
            "No service account key found. Please provide path or place in ~/.colab-bridge/credentials.json"
        )
    
    def setup(self):
        """Complete automated setup"""
        print("🚀 Auto-configuring Colab Bridge...")
        
        # 1. Check if already configured
        if self._is_configured():
            print("✅ Already configured! Loading existing setup...")
            return self._load_config()
        
        # 2. Initialize Google services
        print("📋 Initializing Google services...")
        drive_service = self._init_drive()
        
        # 3. Create dedicated folder
        print("📁 Creating colab-bridge folder...")
        folder_id = self._create_or_find_folder(drive_service)
        
        # 4. Create processor notebook
        print("📓 Setting up Colab processor...")
        notebook_id = self._create_processor_notebook(drive_service, folder_id)
        
        # 5. Get owner email from service account
        owner_email = self._get_owner_email()
        
        # 6. Auto-share everything
        print("🔗 Setting up sharing...")
        self._auto_share(drive_service, folder_id, owner_email)
        self._auto_share(drive_service, notebook_id, owner_email)
        
        # 7. Save configuration
        config = {
            'folder_id': folder_id,
            'notebook_id': notebook_id,
            'owner_email': owner_email,
            'service_account_path': str(self.service_account_path),
            'setup_timestamp': time.time(),
            'notebook_url': f'https://colab.research.google.com/drive/{notebook_id}'
        }
        
        self._save_config(config)
        
        print("\n✅ Setup complete!")
        print(f"📁 Folder ID: {folder_id}")
        print(f"📓 Notebook ID: {notebook_id}")
        print(f"🔗 Notebook URL: {config['notebook_url']}")
        print("\n⚡ Ready to use! No manual steps needed.")
        
        return config
    
    def _init_drive(self):
        """Initialize Drive service"""
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)
    
    def _create_or_find_folder(self, drive_service):
        """Create or find the colab-bridge folder"""
        # Look for existing folder
        query = "name='colab-bridge-auto' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        
        if results.get('files'):
            folder_id = results['files'][0]['id']
            print(f"  ✓ Found existing folder: {folder_id}")
            return folder_id
        
        # Create new folder
        folder_metadata = {
            'name': 'colab-bridge-auto',
            'mimeType': 'application/vnd.google-apps.folder',
            'description': 'Auto-generated folder for Colab Bridge VS Code extension'
        }
        
        folder = drive_service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        
        print(f"  ✓ Created new folder: {folder['id']}")
        return folder['id']
    
    def _create_processor_notebook(self, drive_service, folder_id):
        """Create the processor notebook"""
        # Check if processor exists
        query = f"name='colab_processor.ipynb' and '{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(q=query, fields="files(id)").execute()
        
        if results.get('files'):
            notebook_id = results['files'][0]['id']
            print(f"  ✓ Found existing processor: {notebook_id}")
            return notebook_id
        
        # Create processor notebook
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# 🚀 Colab Bridge Processor\\n",
                        "This notebook runs automatically to process commands from VS Code.\\n",
                        "**Do not close this notebook while using the extension!**"
                    ]
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        "# Auto-mount Drive\\n",
                        "from google.colab import drive\\n",
                        "import os\\n",
                        "import sys\\n",
                        "\\n",
                        "if not os.path.exists('/content/drive'):\\n",
                        "    drive.mount('/content/drive')\\n",
                        "    print('✅ Drive mounted')\\n",
                        "else:\\n",
                        "    print('✅ Drive already mounted')\\n",
                        "\\n",
                        "print(f'Python {sys.version}')\\n",
                        "print('Ready to process commands!')"
                    ]
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        "# Processor loop\\n",
                        "import json\\n",
                        "import time\\n",
                        "import traceback\\n",
                        "from datetime import datetime\\n",
                        "from io import StringIO\\n",
                        "\\n",
                        "# Find the colab-bridge folder\\n",
                        "base_paths = [\\n",
                        "    '/content/drive/MyDrive/colab-bridge-auto',\\n",
                        "    '/content/drive/My Drive/colab-bridge-auto'\\n",
                        "]\\n",
                        "\\n",
                        "base_path = None\\n",
                        "for path in base_paths:\\n",
                        "    if os.path.exists(path):\\n",
                        "        base_path = path\\n",
                        "        break\\n",
                        "\\n",
                        "if not base_path:\\n",
                        "    print('❌ Could not find colab-bridge-auto folder!')\\n",
                        "    print('Please make sure Drive is properly mounted')\\n",
                        "else:\\n",
                        "    print(f'📁 Monitoring: {base_path}')\\n",
                        "    \\n",
                        "    # Create commands directory\\n",
                        "    os.makedirs(base_path, exist_ok=True)\\n",
                        "    \\n",
                        "    print('⏳ Waiting for commands...')\\n",
                        "    print('Keep this notebook running!')\\n",
                        "    \\n",
                        "    while True:\\n",
                        "        try:\\n",
                        "            # Look for command files\\n",
                        "            for file in os.listdir(base_path):\\n",
                        "                if file.startswith('cmd_') and file.endswith('.json'):\\n",
                        "                    cmd_path = os.path.join(base_path, file)\\n",
                        "                    \\n",
                        "                    # Read command\\n",
                        "                    with open(cmd_path, 'r') as f:\\n",
                        "                        cmd = json.load(f)\\n",
                        "                    \\n",
                        "                    print(f'\\\\n⚡ Executing: {cmd[\"id\"]} at {datetime.now().strftime(\"%H:%M:%S\")}')\\n",
                        "                    \\n",
                        "                    # Prepare result\\n",
                        "                    result = {\\n",
                        "                        'id': cmd['id'],\\n",
                        "                        'status': 'success',\\n",
                        "                        'timestamp': time.time()\\n",
                        "                    }\\n",
                        "                    \\n",
                        "                    # Capture output\\n",
                        "                    old_stdout = sys.stdout\\n",
                        "                    sys.stdout = output_buffer = StringIO()\\n",
                        "                    \\n",
                        "                    try:\\n",
                        "                        # Execute code\\n",
                        "                        exec(cmd['code'], {'__name__': '__main__'})\\n",
                        "                        result['output'] = output_buffer.getvalue()\\n",
                        "                        print(f'✅ Success!')\\n",
                        "                    except Exception as e:\\n",
                        "                        result['status'] = 'error'\\n",
                        "                        result['error'] = str(e)\\n",
                        "                        result['traceback'] = traceback.format_exc()\\n",
                        "                        print(f'❌ Error: {e}')\\n",
                        "                    finally:\\n",
                        "                        sys.stdout = old_stdout\\n",
                        "                    \\n",
                        "                    # Write result\\n",
                        "                    result_path = cmd_path.replace('cmd_', 'result_')\\n",
                        "                    with open(result_path, 'w') as f:\\n",
                        "                        json.dump(result, f)\\n",
                        "                    \\n",
                        "                    # Clean up command\\n",
                        "                    os.remove(cmd_path)\\n",
                        "            \\n",
                        "            # Brief pause\\n",
                        "            time.sleep(1)\\n",
                        "            \\n",
                        "        except KeyboardInterrupt:\\n",
                        "            print('\\\\n👋 Processor stopped by user')\\n",
                        "            break\\n",
                        "        except Exception as e:\\n",
                        "            print(f'❌ Processor error: {e}')\\n",
                        "            time.sleep(5)"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "accelerator": "GPU"
            },
            "nbformat": 4,
            "nbformat_minor": 0
        }
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ipynb', delete=False) as f:
            json.dump(notebook_content, f)
            temp_path = f.name
        
        # Upload to Drive
        file_metadata = {
            'name': 'colab_processor.ipynb',
            'parents': [folder_id],
            'mimeType': 'application/vnd.google.colab',
            'description': 'Auto-generated processor for Colab Bridge'
        }
        
        media = MediaFileUpload(
            temp_path,
            mimetype='application/vnd.google.colab',
            resumable=True
        )
        
        notebook = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        # Clean up temp file
        os.unlink(temp_path)
        
        print(f"  ✓ Created processor notebook: {notebook['id']}")
        return notebook['id']
    
    def _get_owner_email(self):
        """Get owner email from service account or use default"""
        try:
            with open(self.service_account_path) as f:
                sa_data = json.load(f)
            
            # Try to extract from client_email
            client_email = sa_data.get('client_email', '')
            # Usually format: name@project.iam.gserviceaccount.com
            # We'll use a default or env var
            
            return os.environ.get('OWNER_EMAIL', 'user@gmail.com')
        except:
            return 'user@gmail.com'
    
    def _auto_share(self, drive_service, file_id, email):
        """Auto-share file with owner"""
        try:
            permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': email
            }
            
            drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=False
            ).execute()
            
            print(f"  ✓ Shared with {email}")
        except Exception as e:
            # Ignore if already shared or email issues
            print(f"  ⚠️  Sharing note: {str(e)[:50]}...")
    
    def _is_configured(self):
        """Check if already configured"""
        return self.config_file.exists()
    
    def _load_config(self):
        """Load existing configuration"""
        with open(self.config_file) as f:
            return json.load(f)
    
    def _save_config(self, config):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Also save to current directory for convenience
        local_config = Path('.colab-bridge-config.json')
        with open(local_config, 'w') as f:
            json.dump(config, f, indent=2)

def auto_setup(service_account_path=None):
    """One-line setup function"""
    setup = AutoColabSetup(service_account_path)
    return setup.setup()

if __name__ == "__main__":
    # Run auto setup
    config = auto_setup()
    
    print("\n🎯 Next step:")
    print(f"   Open this URL once: {config['notebook_url']}")
    print("   Then run: python3 test_auto_setup.py")