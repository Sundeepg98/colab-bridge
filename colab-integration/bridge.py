#!/usr/bin/env python3
"""
Claude Tools - Colab Bridge
Simple, clean bridge for Claude instances to use Google Colab
"""

import os
import json
import time
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

class ClaudeColabBridge:
    """Simple bridge for Claude to execute code in Google Colab"""
    
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.drive_service = None
        self.folder_id = self.config.get('google_drive_folder_id')
        self.instance_id = f"claude_{int(time.time())}"
        
    def _load_config(self, config_path):
        """Load configuration from environment or file"""
        return {
            'service_account_path': os.getenv('SERVICE_ACCOUNT_PATH'),
            'google_drive_folder_id': os.getenv('GOOGLE_DRIVE_FOLDER_ID'),
            'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
            'openai_api_key': os.getenv('OPENAI_API_KEY', '')
        }
    
    def initialize(self):
        """Initialize Google Drive connection"""
        if not self.config['service_account_path']:
            raise ValueError("SERVICE_ACCOUNT_PATH environment variable required")
        
        credentials = service_account.Credentials.from_service_account_file(
            self.config['service_account_path'],
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.drive_service = build('drive', 'v3', credentials=credentials)
        print(f"✅ Claude Tools bridge initialized: {self.instance_id}")
        
    def execute_code(self, code, timeout=30):
        """Execute Python code in Colab"""
        if not self.drive_service:
            self.initialize()
            
        # Create command file
        command = {
            'id': f"cmd_{self.instance_id}_{int(time.time())}",
            'type': 'execute_code',
            'code': code,
            'timestamp': time.time()
        }
        
        # Upload command
        self._upload_json(f"command_{command['id']}.json", command)
        
        # Wait for result
        result = self._wait_for_result(command['id'], timeout)
        return result
    
    def _upload_json(self, filename, data):
        """Upload JSON data to Google Drive"""
        temp_file = f"/tmp/{filename}"
        with open(temp_file, 'w') as f:
            json.dump(data, f)
            
        media = MediaFileUpload(temp_file, mimetype='application/json')
        file_metadata = {
            'name': filename,
            'parents': [self.folder_id]
        }
        
        self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        os.remove(temp_file)
    
    def _wait_for_result(self, command_id, timeout):
        """Wait for command result"""
        start_time = time.time()
        result_filename = f"result_{command_id}.json"
        
        while time.time() - start_time < timeout:
            # Search for result file
            results = self.drive_service.files().list(
                q=f"name='{result_filename}' and parents in '{self.folder_id}'",
                fields='files(id, name)'
            ).execute()
            
            files = results.get('files', [])
            if files:
                # Download and parse result
                file_id = files[0]['id']
                request = self.drive_service.files().get_media(fileId=file_id)
                
                downloaded = io.BytesIO()
                downloader = MediaIoBaseDownload(downloaded, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                
                # Clean up result file
                self.drive_service.files().delete(fileId=file_id).execute()
                
                # Parse result
                downloaded.seek(0)
                result = json.loads(downloaded.read().decode())
                return result
                
            time.sleep(1)
        
        raise TimeoutError(f"Command {command_id} timed out after {timeout}s")

# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python bridge.py '<python_code>'")
        sys.exit(1)
    
    code = sys.argv[1]
    bridge = ClaudeColabBridge()
    
    try:
        result = bridge.execute_code(code)
        print("Result:", result.get('output', 'No output'))
        if result.get('error'):
            print("Error:", result['error'])
    except Exception as e:
        print(f"Bridge error: {e}")