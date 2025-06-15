#!/usr/bin/env python3
"""
Universal Colab Bridge
Works with any coding assistant, CLI tool, or Python application
"""

import os
import json
import time
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # If python-dotenv is not available, try to load manually
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

class UniversalColabBridge:
    """Universal bridge for any tool to execute code in Google Colab"""
    
    def __init__(self, tool_name="universal", config_path=None):
        self.tool_name = tool_name
        self.config = self._load_config(config_path)
        self.drive_service = None
        self.folder_id = self.config.get('google_drive_folder_id')
        self.instance_id = f"{tool_name}_{int(time.time())}"
        
    def _load_config(self, config_path):
        """Load configuration from environment or file"""
        return {
            'service_account_path': os.getenv('SERVICE_ACCOUNT_PATH'),
            'google_drive_folder_id': os.getenv('GOOGLE_DRIVE_FOLDER_ID'),
            'tool_name': self.tool_name
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
        print(f"✅ Universal Colab Bridge initialized: {self.instance_id}")
        
    def execute_code(self, code, timeout=30):
        """Execute Python code in Colab"""
        if not self.drive_service:
            self.initialize()
            
        # Create command
        command = {
            'id': f"cmd_{self.instance_id}_{int(time.time())}",
            'type': 'execute',
            'code': code,
            'timestamp': time.time(),
            'tool': self.tool_name
        }
        
        # Write command file to Drive
        self._write_command(command)
        
        # Wait for result
        try:
            result = self._wait_for_result(command['id'], timeout)
            return result
        except TimeoutError:
            return {
                'status': 'pending',
                'request_id': command['id'],
                'message': f'Request queued for processing by {self.tool_name}'
            }
    
    def _write_command(self, command):
        """Write command to Google Drive"""
        file_name = f"command_{command['id']}.json"
        
        file_metadata = {
            'name': file_name,
            'parents': [self.folder_id]
        }
        
        # Create temporary file for upload
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(command, f, indent=2)
            temp_path = f.name
        
        try:
            media = MediaFileUpload(temp_path, mimetype='application/json')
            
            self.drive_service.files().create(
                body=file_metadata,
                media_body=media
            ).execute()
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
    
    def _wait_for_result(self, command_id, timeout):
        """Wait for result file"""
        start_time = time.time()
        result_name = f"result_{command_id}.json"
        
        while time.time() - start_time < timeout:
            # Look for result file
            query = f"name='{result_name}' and '{self.folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(q=query, fields="files(id)").execute()
            
            files = results.get('files', [])
            if files:
                # Read result
                content = self.drive_service.files().get_media(fileId=files[0]['id']).execute()
                result = json.loads(content.decode('utf-8'))
                
                # Clean up result file
                self.drive_service.files().delete(fileId=files[0]['id']).execute()
                
                return result
            
            time.sleep(1)
        
        raise TimeoutError(f"Command {command_id} timed out after {timeout}s")

# Backward compatibility alias
ClaudeColabBridge = UniversalColabBridge

class CursorColabBridge(UniversalColabBridge):
    """Cursor-specific bridge"""
    def __init__(self, config_path=None):
        super().__init__(tool_name="cursor", config_path=config_path)

class VSCodeColabBridge(UniversalColabBridge):
    """VS Code-specific bridge"""
    def __init__(self, config_path=None):
        super().__init__(tool_name="vscode", config_path=config_path)

class CLIColabBridge(UniversalColabBridge):
    """Generic CLI tool bridge"""
    def __init__(self, cli_name="cli", config_path=None):
        super().__init__(tool_name=cli_name, config_path=config_path)

# Example usage for different tools
def demo_universal_usage():
    """Show how any tool can use the bridge"""
    
    print("🌍 Universal Colab Bridge Demo")
    print("=" * 50)
    
    # Example 1: Claude Code
    claude_bridge = UniversalColabBridge(tool_name="claude")
    claude_bridge.initialize()
    
    # Example 2: Cursor
    cursor_bridge = CursorColabBridge()
    
    # Example 3: Custom CLI
    my_cli_bridge = CLIColabBridge(cli_name="my_awesome_cli")
    
    # Example 4: Any Python app
    app_bridge = UniversalColabBridge(tool_name="my_python_app")
    
    # All use the same interface
    test_code = 'print(f"Hello from {tool_name}!")'
    
    print("All tools use the same execute_code() interface:")
    print("  claude_bridge.execute_code(code)")
    print("  cursor_bridge.execute_code(code)")
    print("  my_cli_bridge.execute_code(code)")
    print("  app_bridge.execute_code(code)")

if __name__ == "__main__":
    demo_universal_usage()