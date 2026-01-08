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
        # Only print in debug mode to avoid breaking tool parsing
        if os.environ.get('COLAB_BRIDGE_DEBUG'):
            import sys
            print(f"✅ Universal Colab Bridge initialized: {self.instance_id}", file=sys.stderr)
        
    def execute_code(self, code, timeout=30, return_format='dict'):
        """Execute Python code in Colab
        
        Args:
            code: Python code to execute
            timeout: Timeout in seconds
            return_format: 'dict' for normal dict, 'vscode' for VS Code compatible output
        """
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
        
        # Store command_id for reference
        self.command_id = command['id']
        
        # Write command file to Drive (takes ~2 seconds)
        try:
            upload_start = time.time()
            self._write_command(command)
            upload_time = time.time() - upload_start
            # Only print timing in debug mode or to stderr to avoid breaking VS Code parsing
            if upload_time > 1 and os.environ.get('COLAB_BRIDGE_DEBUG'):
                import sys
                print(f"📤 Command uploaded in {upload_time:.1f}s", file=sys.stderr)
        except Exception as e:
            print(f"❌ Error writing command: {e}")
            raise
        
        # Wait for result
        try:
            result = self._wait_for_result(command['id'], timeout)
            
            # If VS Code format requested, convert visualizations to text
            if return_format == 'vscode' and result.get('visualizations'):
                # For now, add a note about visualizations in text output
                viz_count = len(result['visualizations'])
                result['output'] = result.get('output', '') + f"\n\n[{viz_count} visualization(s) captured - enhanced display coming soon]"
                
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
    
    def _create_command_file(self, code):
        """Create command file (compatibility method)"""
        command = {
            'id': f"cmd_{self.instance_id}_{int(time.time())}",
            'type': 'execute',
            'code': code,
            'timestamp': time.time(),
            'tool': self.tool_name
        }
        self.command_id = command['id']
        self._write_command(command)
        return command
    
    def _wait_for_result(self, command_id, timeout):
        """Wait for result file with instant polling"""
        start_time = time.time()
        poll_count = 0
        
        while time.time() - start_time < timeout:
            poll_count += 1
            
            # Look for result file - use contains to catch any pattern
            # The processor might create result_result_ID or other variations
            base_id = command_id.replace('cmd_', '')
            query = f"name contains '{base_id}' and name contains 'result' and '{self.folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get('files', [])
                    
            if files:
                # Read result
                content = self.drive_service.files().get_media(fileId=files[0]['id']).execute()
                result = json.loads(content.decode('utf-8'))
                
                # Clean up result file
                self.drive_service.files().delete(fileId=files[0]['id']).execute()
                
                # Log timing for debugging
                elapsed = time.time() - start_time
                if elapsed < 1:
                    print(f"⚡ Got result in {elapsed:.3f}s after {poll_count} polls")
                
                return result
            
            # Smart polling based on actual Drive API performance
            # Each API call takes ~400ms, so we adjust sleep times accordingly
            elapsed = time.time() - start_time
            
            if elapsed < 3:
                # First 3 seconds: No sleep needed
                # API call itself takes 400ms, giving us ~7 polls in 3 seconds
                pass
            elif elapsed < 10:
                # 3-10 seconds: Add small delay
                time.sleep(0.2)  # Total ~600ms between polls
            elif elapsed < 30:
                # 10-30 seconds: Poll every second
                time.sleep(0.6)  # Total ~1s between polls (400ms API + 600ms sleep)
            else:
                # After 30 seconds: Poll every 2 seconds
                time.sleep(1.6)  # Total ~2s between polls
        
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