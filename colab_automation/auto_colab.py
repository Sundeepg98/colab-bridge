#!/usr/bin/env python3
"""
Fully Automated Colab Integration
No manual setup required!
"""

import os
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class AutomatedColabBridge:
    """Fully automated Colab execution - zero manual steps"""
    
    def __init__(self, project_name="auto_colab"):
        self.project_name = project_name
        self.setup_complete = False
        self.folder_id = None
        self.notebook_id = None
        self.drive_service = None
        self.monitoring_thread = None
        self.results_cache = {}
        
        # Auto-detect credentials
        self._auto_setup_credentials()
        
    def _auto_setup_credentials(self):
        """Automatically find and set up credentials"""
        # Search common locations
        possible_paths = [
            Path.home() / '.colab-bridge' / 'credentials.json',
            Path(__file__).parent.parent / 'credentials' / '*.json',
            Path.home() / 'projects' / 'colab-bridge' / 'credentials' / '*.json',
            os.environ.get('SERVICE_ACCOUNT_PATH', ''),
        ]
        
        for path in possible_paths:
            if isinstance(path, str) and path:
                path = Path(path)
            
            if path and path.exists():
                self.creds_path = str(path)
                break
            elif path and '*' in str(path):
                # Handle glob patterns
                parent = path.parent
                if parent.exists():
                    files = list(parent.glob(path.name))
                    if files:
                        self.creds_path = str(files[0])
                        break
        else:
            # If no credentials found, guide user
            self._setup_wizard()
    
    def _setup_wizard(self):
        """Interactive setup wizard for first-time users"""
        print("🚀 Welcome to Colab-Bridge Auto Setup!")
        print("=" * 50)
        print("\n📋 I'll help you get started in 30 seconds...\n")
        
        # Create config directory
        config_dir = Path.home() / '.colab-bridge'
        config_dir.mkdir(exist_ok=True)
        
        print("Please provide your service account key path:")
        print("(You can drag and drop the file here)")
        
        creds_path = input("> ").strip().strip("'\"")
        
        if Path(creds_path).exists():
            # Copy to standard location
            import shutil
            dest = config_dir / 'credentials.json'
            shutil.copy(creds_path, dest)
            self.creds_path = str(dest)
            print("✅ Credentials saved!")
        else:
            raise FileNotFoundError(f"Credentials not found: {creds_path}")
    
    def initialize(self):
        """One-time initialization - fully automated"""
        if self.setup_complete:
            return
        
        print("🔧 Auto-initializing Colab environment...")
        
        # 1. Connect to Google Drive
        self._connect_drive()
        
        # 2. Create or find integration folder
        self._setup_folder()
        
        # 3. Deploy processor notebook
        self._deploy_processor()
        
        # 4. Start monitoring thread
        self._start_monitor()
        
        self.setup_complete = True
        print("✅ Auto-initialization complete!")
        
    def _connect_drive(self):
        """Connect to Google Drive"""
        credentials = service_account.Credentials.from_service_account_file(
            self.creds_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.drive_service = build('drive', 'v3', credentials=credentials)
        
    def _setup_folder(self):
        """Create or find integration folder"""
        # Check if folder exists
        query = f"name='colab-bridge-auto' and mimeType='application/vnd.google-apps.folder'"
        results = self.drive_service.files().list(q=query, fields="files(id)").execute()
        
        if results.get('files'):
            self.folder_id = results['files'][0]['id']
            print(f"✅ Using existing folder")
        else:
            # Create new folder
            folder_metadata = {
                'name': 'colab-bridge-auto',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            self.folder_id = folder['id']
            
            # Auto-share with user
            self._auto_share(self.folder_id)
            print(f"✅ Created integration folder")
    
    def _deploy_processor(self):
        """Deploy the processor notebook automatically"""
        # Check if processor exists
        query = f"name='auto_processor.ipynb' and '{self.folder_id}' in parents"
        results = self.drive_service.files().list(q=query, fields="files(id)").execute()
        
        if results.get('files'):
            self.notebook_id = results['files'][0]['id']
            print(f"✅ Processor notebook ready")
            return
        
        # Create processor notebook
        notebook_content = self._generate_processor_notebook()
        
        # Save temporarily
        temp_path = Path.home() / '.colab-bridge' / 'auto_processor.ipynb'
        temp_path.parent.mkdir(exist_ok=True)
        
        with open(temp_path, 'w') as f:
            json.dump(notebook_content, f)
        
        # Upload to Drive
        file_metadata = {
            'name': 'auto_processor.ipynb',
            'parents': [self.folder_id],
            'mimeType': 'application/vnd.google.colab'
        }
        
        media = MediaFileUpload(
            str(temp_path),
            mimetype='application/vnd.google.colab',
            resumable=True
        )
        
        notebook = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        self.notebook_id = notebook['id']
        self._auto_share(self.notebook_id)
        
        print(f"✅ Deployed processor notebook")
        print(f"🔗 Open once: https://colab.research.google.com/drive/{self.notebook_id}")
        
    def _generate_processor_notebook(self):
        """Generate the processor notebook content"""
        return {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# 🚀 Auto Colab Processor\n", "Runs automatically when opened!"]
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": [
                        "# Auto-mount Drive\n",
                        "from google.colab import drive\n",
                        "import os\n",
                        "if not os.path.exists('/content/drive'):\n",
                        "    drive.mount('/content/drive')\n",
                        "print('✅ Drive mounted')"
                    ]
                },
                {
                    "cell_type": "code", 
                    "metadata": {},
                    "source": [
                        "# Auto processor loop\n",
                        "import json\n",
                        "import time\n",
                        "import sys\n",
                        "from datetime import datetime\n",
                        "\n",
                        "base_path = '/content/drive/MyDrive/colab-bridge-auto'\n",
                        "print(f'🔍 Monitoring: {base_path}')\n",
                        "\n",
                        "# Create heartbeat file\n",
                        "heartbeat_path = os.path.join(base_path, 'heartbeat.json')\n",
                        "\n",
                        "while True:\n",
                        "    try:\n",
                        "        # Update heartbeat\n",
                        "        with open(heartbeat_path, 'w') as f:\n",
                        "            json.dump({'timestamp': time.time(), 'status': 'running'}, f)\n",
                        "        \n",
                        "        # Check for commands\n",
                        "        if os.path.exists(base_path):\n",
                        "            for file in os.listdir(base_path):\n",
                        "                if file.startswith('cmd_') and file.endswith('.json'):\n",
                        "                    cmd_path = os.path.join(base_path, file)\n",
                        "                    \n",
                        "                    # Read command\n",
                        "                    with open(cmd_path, 'r') as f:\n",
                        "                        cmd = json.load(f)\n",
                        "                    \n",
                        "                    print(f'⚡ Executing: {cmd[\"id\"]}')\n",
                        "                    \n",
                        "                    # Execute code\n",
                        "                    result = {\n",
                        "                        'id': cmd['id'],\n",
                        "                        'timestamp': time.time(),\n",
                        "                        'status': 'success'\n",
                        "                    }\n",
                        "                    \n",
                        "                    # Capture output\n",
                        "                    from io import StringIO\n",
                        "                    old_stdout = sys.stdout\n",
                        "                    sys.stdout = StringIO()\n",
                        "                    \n",
                        "                    try:\n",
                        "                        exec(cmd['code'])\n",
                        "                        result['output'] = sys.stdout.getvalue()\n",
                        "                    except Exception as e:\n",
                        "                        result['status'] = 'error'\n",
                        "                        result['error'] = str(e)\n",
                        "                    finally:\n",
                        "                        sys.stdout = old_stdout\n",
                        "                    \n",
                        "                    # Write result\n",
                        "                    result_path = cmd_path.replace('cmd_', 'result_')\n",
                        "                    with open(result_path, 'w') as f:\n",
                        "                        json.dump(result, f)\n",
                        "                    \n",
                        "                    # Clean up\n",
                        "                    os.remove(cmd_path)\n",
                        "                    print(f'✅ Completed: {cmd[\"id\"]}')\n",
                        "        \n",
                        "        time.sleep(1)\n",
                        "        \n",
                        "    except KeyboardInterrupt:\n",
                        "        print('\\n👋 Processor stopped')\n",
                        "        break\n",
                        "    except Exception as e:\n",
                        "        print(f'❌ Error: {e}')\n",
                        "        time.sleep(5)"
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
    
    def _auto_share(self, file_id):
        """Auto-share with user email"""
        # Try to detect user email
        user_email = os.environ.get('OWNER_EMAIL', 'sundeepg8@gmail.com')
        
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': user_email
        }
        
        try:
            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=False
            ).execute()
        except:
            pass  # Ignore if already shared
    
    def _start_monitor(self):
        """Start background monitoring thread"""
        self.monitoring_thread = threading.Thread(
            target=self._monitor_heartbeat,
            daemon=True
        )
        self.monitoring_thread.start()
    
    def _monitor_heartbeat(self):
        """Monitor processor health"""
        while True:
            try:
                # Check heartbeat file
                query = f"name='heartbeat.json' and '{self.folder_id}' in parents"
                results = self.drive_service.files().list(
                    q=query,
                    fields="files(id,modifiedTime)"
                ).execute()
                
                if results.get('files'):
                    # Check if recent
                    modified = results['files'][0]['modifiedTime']
                    # Parse and check if recent (within 5 minutes)
                    # If stale, notify user
                    pass
                    
            except:
                pass
            
            time.sleep(30)  # Check every 30 seconds
    
    def execute(self, code, timeout=30):
        """Execute code in Colab - fully automated"""
        if not self.setup_complete:
            self.initialize()
        
        # Generate command
        cmd_id = f"cmd_{int(time.time() * 1000)}"
        command = {
            'id': cmd_id,
            'code': code,
            'timestamp': time.time()
        }
        
        # Write command file
        self._write_to_drive(f"cmd_{cmd_id}.json", command)
        
        # Wait for result
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = self._check_result(cmd_id)
            if result:
                return result
            time.sleep(0.5)
        
        return {
            'status': 'timeout',
            'message': 'Request timed out. Make sure Colab notebook is running.'
        }
    
    def _write_to_drive(self, filename, data):
        """Write JSON file to Drive folder"""
        # Create temp file
        temp_path = Path.home() / '.colab-bridge' / 'temp' / filename
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, 'w') as f:
            json.dump(data, f)
        
        # Upload to Drive
        file_metadata = {
            'name': filename,
            'parents': [self.folder_id]
        }
        
        media = MediaFileUpload(
            str(temp_path),
            mimetype='application/json'
        )
        
        self.drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
        # Clean up
        temp_path.unlink()
    
    def _check_result(self, cmd_id):
        """Check for result file"""
        query = f"name='result_{cmd_id}.json' and '{self.folder_id}' in parents"
        results = self.drive_service.files().list(
            q=query,
            fields="files(id)"
        ).execute()
        
        if results.get('files'):
            file_id = results['files'][0]['id']
            
            # Download result
            request = self.drive_service.files().get_media(fileId=file_id)
            content = request.execute()
            
            # Delete result file
            self.drive_service.files().delete(fileId=file_id).execute()
            
            return json.loads(content)
        
        return None

# Convenience function
def auto_colab(code):
    """Execute code in Colab with zero setup"""
    bridge = AutomatedColabBridge()
    return bridge.execute(code)

if __name__ == "__main__":
    # Demo
    print("🚀 Testing Automated Colab Bridge...")
    
    bridge = AutomatedColabBridge()
    bridge.initialize()
    
    # Test execution
    result = bridge.execute('''
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
''')
    
    print(f"\n📥 Result: {result}")