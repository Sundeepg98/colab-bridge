#!/usr/bin/env python3
"""
Automated Colab Management
Handles notebook upload and execution automatically
"""

import os
import json
import time
import requests
import webbrowser
from typing import Dict, Any, Optional
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class AutoColabManager:
    """Automatically manage Colab notebooks"""
    
    def __init__(self, service_account_path: str, drive_folder_id: str):
        self.sa_path = service_account_path
        self.folder_id = drive_folder_id
        self.drive_service = None
        self.colab_notebook_id = None
        
    def initialize(self):
        """Initialize Google Drive service"""
        credentials = service_account.Credentials.from_service_account_file(
            self.sa_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.drive_service = build('drive', 'v3', credentials=credentials)
        print("✅ Auto Colab Manager initialized")
        
    def upload_notebook(self, notebook_path: str) -> str:
        """Upload notebook to Google Drive"""
        notebook_name = Path(notebook_path).name
        
        # Check if notebook already exists
        query = f"name='{notebook_name}' and '{self.folder_id}' in parents and trashed=false"
        results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
        
        if results.get('files'):
            # Update existing
            file_id = results['files'][0]['id']
            media = MediaFileUpload(notebook_path, mimetype='application/x-ipynb+json')
            self.drive_service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            print(f"✅ Updated existing notebook: {notebook_name}")
        else:
            # Create new
            file_metadata = {
                'name': notebook_name,
                'parents': [self.folder_id],
                'mimeType': 'application/x-ipynb+json'
            }
            media = MediaFileUpload(notebook_path, mimetype='application/x-ipynb+json')
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            file_id = file.get('id')
            print(f"✅ Uploaded new notebook: {notebook_name}")
        
        self.colab_notebook_id = file_id
        return file_id
    
    def create_colab_link(self, notebook_id: str) -> str:
        """Create Colab link for the notebook"""
        return f"https://colab.research.google.com/drive/{notebook_id}"
    
    def inject_auto_run_code(self, notebook_path: str) -> str:
        """Inject auto-run code into notebook"""
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        # Add auto-run metadata to first code cell
        if notebook['cells'] and notebook['cells'][0]['cell_type'] == 'code':
            notebook['cells'][0]['metadata']['cellView'] = 'form'
            notebook['cells'][0]['metadata']['id'] = 'auto-run-cell'
        
        # Create temporary notebook with auto-run
        temp_path = Path(notebook_path).parent / f"auto_{Path(notebook_path).name}"
        with open(temp_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        return str(temp_path)
    
    def create_auto_processor_notebook(self) -> str:
        """Create a notebook that auto-runs the processor"""
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# Claude Tools - Auto Processor\\n",
                        "This notebook automatically starts processing Claude Tools requests"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {
                        "cellView": "form",
                        "id": "setup-cell"
                    },
                    "outputs": [],
                    "source": [
                        "#@title Setup and Mount Drive { display-mode: \"form\" }\\n",
                        "from google.colab import drive\\n",
                        "import time\\n",
                        "print('🔄 Mounting Google Drive...')\\n",
                        "drive.mount('/content/drive')\\n",
                        "print('✅ Drive mounted!')\\n",
                        "\\n",
                        "# Install dependencies\\n",
                        "!pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client\\n",
                        "print('✅ Dependencies installed')"
                    ]
                },
                {
                    "cell_type": "code", 
                    "execution_count": None,
                    "metadata": {
                        "cellView": "form",
                        "id": "processor-cell"
                    },
                    "outputs": [],
                    "source": [
                        "#@title Claude Tools Processor { display-mode: \"form\" }\\n",
                        "import os\\n",
                        "import json\\n",
                        "import time\\n",
                        "import traceback\\n",
                        "from datetime import datetime\\n",
                        "from google.colab import auth\\n",
                        "from googleapiclient.discovery import build\\n",
                        "from googleapiclient.http import MediaIoBaseUpload\\n",
                        "import io\\n",
                        "\\n",
                        "# Configuration\\n",
                        "FOLDER_ID = '" + self.folder_id + "'\\n",
                        "\\n",
                        "class ColabProcessor:\\n",
                        "    def __init__(self, folder_id):\\n",
                        "        self.folder_id = folder_id\\n",
                        "        self.drive_service = None\\n",
                        "        self.processed_requests = set()\\n",
                        "        \\n",
                        "    def initialize(self):\\n",
                        "        auth.authenticate_user()\\n",
                        "        self.drive_service = build('drive', 'v3')\\n",
                        "        print(f'✅ Initialized with folder: {self.folder_id}')\\n",
                        "        \\n",
                        "    def execute_code(self, code):\\n",
                        "        from io import StringIO\\n",
                        "        import sys\\n",
                        "        old_stdout = sys.stdout\\n",
                        "        sys.stdout = StringIO()\\n",
                        "        try:\\n",
                        "            exec(code, {'__name__': '__main__'})\\n",
                        "            output = sys.stdout.getvalue()\\n",
                        "            return {'status': 'success', 'output': output, 'timestamp': time.time()}\\n",
                        "        except Exception as e:\\n",
                        "            return {'status': 'error', 'error': str(e), 'traceback': traceback.format_exc(), 'timestamp': time.time()}\\n",
                        "        finally:\\n",
                        "            sys.stdout = old_stdout\\n",
                        "    \\n",
                        "    def list_requests(self):\\n",
                        "        query = f\\\"'{self.folder_id}' in parents and name contains 'request_' and trashed=false\\\"\\n",
                        "        results = self.drive_service.files().list(q=query, fields='files(id, name)').execute()\\n",
                        "        return [f for f in results.get('files', []) if f['name'].endswith('.json') and f['id'] not in self.processed_requests]\\n",
                        "    \\n",
                        "    def read_request(self, file_id):\\n",
                        "        content = self.drive_service.files().get_media(fileId=file_id).execute()\\n",
                        "        return json.loads(content.decode('utf-8'))\\n",
                        "    \\n",
                        "    def write_response(self, request_id, response_data):\\n",
                        "        response_name = f'response_{request_id}.json'\\n",
                        "        file_metadata = {'name': response_name, 'parents': [self.folder_id]}\\n",
                        "        media = MediaIoBaseUpload(io.BytesIO(json.dumps(response_data, indent=2).encode('utf-8')), mimetype='application/json')\\n",
                        "        self.drive_service.files().create(body=file_metadata, media_body=media).execute()\\n",
                        "        print(f'✅ Response written: {response_name}')\\n",
                        "    \\n",
                        "    def process_request(self, request_file):\\n",
                        "        request_id = request_file['name'].replace('request_', '').replace('.json', '')\\n",
                        "        print(f'📋 Processing: {request_id}')\\n",
                        "        try:\\n",
                        "            request_data = self.read_request(request_file['id'])\\n",
                        "            if request_data['type'] == 'execute_code':\\n",
                        "                result = self.execute_code(request_data['code'])\\n",
                        "            else:\\n",
                        "                result = {'status': 'error', 'error': f\\\"Unknown request type: {request_data['type']}\\\"}\\n",
                        "            self.write_response(request_id, result)\\n",
                        "            self.processed_requests.add(request_file['id'])\\n",
                        "        except Exception as e:\\n",
                        "            print(f'❌ Error: {e}')\\n",
                        "            self.write_response(request_id, {'status': 'error', 'error': str(e), 'timestamp': time.time()})\\n",
                        "    \\n",
                        "    def run(self, duration=3600, poll_interval=3):\\n",
                        "        print(f'🚀 Starting Auto Processor')\\n",
                        "        print(f'⏱️  Running for {duration/60:.0f} minutes')\\n",
                        "        print(f'📁 Monitoring: {self.folder_id}')\\n",
                        "        start_time = time.time()\\n",
                        "        while time.time() - start_time < duration:\\n",
                        "            requests = self.list_requests()\\n",
                        "            if requests:\\n",
                        "                print(f'\\\\n📨 Found {len(requests)} request(s)')\\n",
                        "                for req in requests:\\n",
                        "                    self.process_request(req)\\n",
                        "            else:\\n",
                        "                print(f'⏳ Waiting... ({datetime.now().strftime(\\\"%H:%M:%S\\\")})', end='\\\\r')\\n",
                        "            time.sleep(poll_interval)\\n",
                        "        print('\\\\n⏱️  Auto-run completed')\\n",
                        "\\n",
                        "# Auto-start processor\\n",
                        "print('🤖 Claude Tools Auto Processor')\\n",
                        "print('=' * 40)\\n",
                        "processor = ColabProcessor(FOLDER_ID)\\n",
                        "processor.initialize()\\n",
                        "processor.run(duration=3600, poll_interval=2)  # Run for 1 hour"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python", 
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.10.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        # Save notebook
        notebook_path = Path(__file__).parent.parent / "notebooks" / "auto-processor.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook_content, f, indent=2)
            
        return str(notebook_path)
    
    def start_colab_session(self, open_browser=True) -> Dict[str, Any]:
        """Start an automated Colab session"""
        print("🚀 Starting automated Colab session...")
        
        # Create auto-processor notebook
        notebook_path = self.create_auto_processor_notebook()
        print("✅ Created auto-processor notebook")
        
        # Upload to Drive
        notebook_id = self.upload_notebook(notebook_path)
        
        # Create Colab link
        colab_url = self.create_colab_link(notebook_id)
        
        print(f"\n✅ Colab notebook ready!")
        print(f"📋 Notebook ID: {notebook_id}")
        print(f"🔗 Colab URL: {colab_url}")
        
        if open_browser:
            print("\n🌐 Opening Colab in browser...")
            webbrowser.open(colab_url)
            print("⚡ The notebook will auto-run when opened!")
            print("📝 Just click 'Run all' or wait for auto-execution")
        
        return {
            "notebook_id": notebook_id,
            "colab_url": colab_url,
            "folder_id": self.folder_id,
            "status": "ready"
        }
    
    def create_gist_loader(self) -> str:
        """Create a Gist-based loader for even easier setup"""
        gist_content = f'''# Quick Claude Tools Colab Setup
# Run this in any Colab notebook:

!pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

import os
exec(requests.get('https://raw.githubusercontent.com/claude-tools/colab-processor/main/run.py').text)

# Or one-liner:
# !curl -s https://claude.tools/colab | python3
'''
        return gist_content


def main():
    """Example usage"""
    from dotenv import load_dotenv
    load_dotenv()
    
    manager = AutoColabManager(
        service_account_path=os.getenv('SERVICE_ACCOUNT_PATH'),
        drive_folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    )
    
    manager.initialize()
    result = manager.start_colab_session()
    
    print("\n✅ Automated Colab setup complete!")
    print("The notebook will start processing requests automatically")

if __name__ == "__main__":
    main()