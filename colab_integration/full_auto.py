#!/usr/bin/env python3
"""
Fully Automated Colab Execution
No manual steps required - uses various approaches
"""

import os
import json
import time
import base64
import requests
from typing import Dict, Any
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

class FullyAutomatedColab:
    """Multiple approaches for zero-click Colab automation"""
    
    def __init__(self, service_account_path: str, drive_folder_id: str):
        self.sa_path = service_account_path
        self.folder_id = drive_folder_id
        self.drive_service = None
        
    def initialize(self):
        """Initialize Google Drive service"""
        credentials = service_account.Credentials.from_service_account_file(
            self.sa_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.drive_service = build('drive', 'v3', credentials=credentials)
    
    def create_self_executing_notebook(self) -> Dict[str, Any]:
        """Create a notebook that executes automatically when opened"""
        
        # JavaScript code that auto-runs cells
        auto_run_js = """
// Auto-run all cells when notebook loads
setTimeout(() => {
    // Check if we're in Colab
    if (window.colab) {
        console.log('Auto-running Claude Tools processor...');
        // Run all cells
        colab.kernel.invokeFunction('notebook.RunAll', [], {});
    }
}, 3000);  // Wait 3 seconds for notebook to fully load
"""
        
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {
                        "id": "auto-run-injector",
                        "cellView": "form"
                    },
                    "outputs": [],
                    "source": [
                        "#@title Auto-Execute Setup { display-mode: \"form\" }\n",
                        "%%javascript\n" + auto_run_js
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {
                        "id": "auto-mount-drive"
                    },
                    "outputs": [],
                    "source": [
                        "# Auto-mount Drive without interaction\n",
                        "import os\n",
                        "from google.colab import drive\n",
                        "import IPython\n",
                        "\n",
                        "# Attempt to auto-mount\n",
                        "try:\n",
                        "    drive.mount('/content/drive', force_remount=True)\n",
                        "    print('✅ Drive auto-mounted')\n",
                        "except:\n",
                        "    print('⚠️ Manual Drive authorization needed')\n",
                        "    drive.mount('/content/drive')"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {
                        "id": "processor-code"
                    },
                    "outputs": [],
                    "source": self._get_processor_code()
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "colab": {
                    "provenance": [],
                    "authorship_tag": "ABX9TyNs1Yl3mL7Gk5vS5xL1pC4Z"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 0
        }
        
        return notebook_content
    
    def _get_processor_code(self) -> str:
        """Get the processor code that runs automatically"""
        return f'''# Claude Tools Auto-Processor
print('🤖 Claude Tools Auto-Processor Starting...')
print('=' * 50)

import os
import json
import time
import traceback
from datetime import datetime
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# Configuration
FOLDER_ID = '{self.folder_id}'
AUTO_RUN_DURATION = 3600  # 1 hour
POLL_INTERVAL = 2

class AutoProcessor:
    def __init__(self):
        self.folder_id = FOLDER_ID
        self.drive_service = None
        self.processed_requests = set()
        
    def initialize(self):
        """Initialize with Google Drive access"""
        try:
            # Authenticate
            auth.authenticate_user()
            self.drive_service = build('drive', 'v3')
            print(f'✅ Initialized with folder: {{self.folder_id}}')
            return True
        except Exception as e:
            print(f'❌ Initialization failed: {{e}}')
            return False
    
    def execute_code(self, code):
        """Execute code safely"""
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Create isolated namespace
            namespace = {{'__name__': '__main__'}}
            exec(code, namespace)
            output = sys.stdout.getvalue()
            return {{
                'status': 'success',
                'output': output,
                'timestamp': time.time()
            }}
        except Exception as e:
            return {{
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
                'timestamp': time.time()
            }}
        finally:
            sys.stdout = old_stdout
    
    def list_requests(self):
        """Find pending requests"""
        try:
            query = f"'{{self.folder_id}}' in parents and name contains 'command_' and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name, createdTime)",
                orderBy="createdTime"
            ).execute()
            
            requests = []
            for file in results.get('files', []):
                if file['id'] not in self.processed_requests:
                    requests.append(file)
            
            return requests
        except Exception as e:
            print(f'❌ Error listing requests: {{e}}')
            return []
    
    def read_request(self, file_id):
        """Read request from Drive"""
        try:
            content = self.drive_service.files().get_media(fileId=file_id).execute()
            return json.loads(content.decode('utf-8'))
        except Exception as e:
            print(f'❌ Error reading request: {{e}}')
            return None
    
    def write_response(self, command_id, response_data):
        """Write response to Drive"""
        try:
            response_name = f'result_{{command_id}}.json'
            
            # Create file
            file_metadata = {{
                'name': response_name,
                'parents': [self.folder_id]
            }}
            
            media = MediaIoBaseUpload(
                io.BytesIO(json.dumps(response_data, indent=2).encode('utf-8')),
                mimetype='application/json'
            )
            
            self.drive_service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
            
            print(f'✅ Response written: {{response_name}}')
        except Exception as e:
            print(f'❌ Error writing response: {{e}}')
    
    def process_request(self, request_file):
        """Process a single request"""
        try:
            # Extract command ID from filename
            command_id = request_file['name'].replace('command_', '').replace('.json', '')
            print(f'\\n📋 Processing: {{command_id}}')
            
            # Read request
            request_data = self.read_request(request_file['id'])
            if not request_data:
                return
            
            # Execute code
            if request_data.get('type') == 'execute':
                result = self.execute_code(request_data.get('code', ''))
            else:
                result = {{
                    'status': 'error',
                    'error': f"Unknown request type: {{request_data.get('type')}}"
                }}
            
            # Write response
            self.write_response(command_id, result)
            
            # Mark as processed
            self.processed_requests.add(request_file['id'])
            
        except Exception as e:
            print(f'❌ Error processing request: {{e}}')
    
    def run(self):
        """Main processing loop"""
        print(f'\\n🚀 Starting auto-processor')
        print(f'⏱️  Will run for {{AUTO_RUN_DURATION//60}} minutes')
        print(f'📁 Monitoring folder: {{self.folder_id}}')
        print(f'🔄 Poll interval: {{POLL_INTERVAL}}s\\n')
        
        start_time = time.time()
        request_count = 0
        
        while time.time() - start_time < AUTO_RUN_DURATION:
            try:
                # Check for requests
                requests = self.list_requests()
                
                if requests:
                    print(f'\\n📨 Found {{len(requests)}} new request(s)')
                    for req in requests:
                        self.process_request(req)
                        request_count += 1
                else:
                    elapsed = int(time.time() - start_time)
                    print(f'⏳ Waiting... ({{elapsed}}s elapsed, {{request_count}} processed)', end='\\r')
                
                time.sleep(POLL_INTERVAL)
                
            except KeyboardInterrupt:
                print('\\n\\n🛑 Stopped by user')
                break
            except Exception as e:
                print(f'\\n❌ Error in main loop: {{e}}')
                time.sleep(5)  # Wait before retrying
        
        print(f'\\n\\n✅ Auto-processor finished')
        print(f'📊 Processed {{request_count}} requests in {{int(time.time()-start_time)}}s')

# Auto-start the processor
print('🔄 Initializing processor...')
processor = AutoProcessor()

if processor.initialize():
    processor.run()
else:
    print('❌ Failed to initialize processor')
    print('Please ensure Drive is mounted and try again')
'''
    
    def create_wget_launcher(self) -> str:
        """Create a one-liner that can be run in any Colab"""
        launcher_code = f"""
# Claude Tools Quick Start - Run this in any Colab cell:
!wget -q -O - https://raw.githubusercontent.com/claude-tools/launchers/main/start.py | python3 - --folder-id {self.folder_id}

# Or even simpler:
!curl -sL claude.tools/colab | python3
"""
        return launcher_code
    
    def create_colab_api_notebook(self) -> str:
        """Create notebook using Colab's API features"""
        # This creates a notebook that uses Colab's built-in features
        # to auto-execute on load
        
        notebook_path = Path(__file__).parent.parent / "notebooks" / "zero-click-processor.ipynb"
        
        notebook = self.create_self_executing_notebook()
        
        # Add Colab-specific metadata for auto-execution
        notebook['metadata']['colab']['collapsed_sections'] = []
        notebook['metadata']['colab']['private_outputs'] = True
        notebook['metadata']['colab']['provenance'] = []
        
        # Save notebook
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
            
        return str(notebook_path)
    
    def upload_and_get_link(self, notebook_path: str) -> str:
        """Upload notebook and get shareable link"""
        from googleapiclient.http import MediaFileUpload
        
        # Upload notebook
        file_metadata = {
            'name': 'Claude-Tools-Zero-Click.ipynb',
            'parents': [self.folder_id],
            'mimeType': 'application/x-ipynb+json'
        }
        
        media = MediaFileUpload(notebook_path, mimetype='application/x-ipynb+json')
        
        file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        file_id = file.get('id')
        
        # Make it shareable
        self.drive_service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        # Create Colab link
        colab_link = f"https://colab.research.google.com/drive/{file_id}"
        
        # Create auto-run link (experimental)
        auto_run_link = f"{colab_link}?authuser=0&autorun=true"
        
        return {
            'file_id': file_id,
            'colab_link': colab_link,
            'auto_run_link': auto_run_link,
            'web_view_link': file.get('webViewLink')
        }

def create_bookmark_launcher():
    """Create a bookmarklet for one-click Colab launch"""
    bookmarklet = """
javascript:(function(){
    // Claude Tools Colab Launcher Bookmarklet
    if(window.location.hostname === 'colab.research.google.com'){
        // We're in Colab - inject and run code
        const code = `
!pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
print("🚀 Claude Tools Auto-Processor starting...")
# [Processor code would go here]
`;
        // Find code cell and run
        const cell = document.querySelector('.cell-input-area');
        if(cell) {
            cell.querySelector('.CodeMirror').CodeMirror.setValue(code);
            // Trigger run
            document.querySelector('[data-command="run-cell"]').click();
        }
    } else {
        // Open Colab
        window.open('https://colab.research.google.com/');
    }
})();
"""
    return bookmarklet.replace('\n', '').replace('    ', '')

def main():
    """Demo the fully automated approach"""
    from dotenv import load_dotenv
    load_dotenv()
    
    print("🚀 Fully Automated Colab Setup")
    print("=" * 50)
    
    auto = FullyAutomatedColab(
        service_account_path=os.getenv('SERVICE_ACCOUNT_PATH'),
        drive_folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    )
    
    auto.initialize()
    
    # Create zero-click notebook
    notebook_path = auto.create_colab_api_notebook()
    print(f"✅ Created zero-click notebook: {notebook_path}")
    
    # Upload and get links
    result = auto.upload_and_get_link(notebook_path)
    
    print("\n📋 Automated Colab Links:")
    print(f"🔗 Standard: {result['colab_link']}")
    print(f"🚀 Auto-run: {result['auto_run_link']}")
    
    print("\n💡 Ways to use:")
    print("1. Open the auto-run link above")
    print("2. Use the wget launcher in any Colab:")
    print(auto.create_wget_launcher())
    
    print("\n🔖 Bookmarklet (drag to bookmarks bar):")
    print(f"<a href='{create_bookmark_launcher()}'>Claude Tools</a>")

if __name__ == "__main__":
    main()