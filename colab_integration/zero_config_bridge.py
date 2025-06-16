#!/usr/bin/env python3
"""
Zero-Config Colab Bridge
Just provide service account key - everything else is automatic!
"""

import os
import json
import time
from pathlib import Path
from .auto_setup import AutoColabSetup
from .universal_bridge import UniversalColabBridge

class ZeroConfigBridge(UniversalColabBridge):
    """Colab Bridge with automatic setup - zero configuration needed!"""
    
    def __init__(self, service_account_path=None):
        # Auto-setup if needed
        self.setup_manager = AutoColabSetup(service_account_path)
        self.auto_config = self.setup_manager.setup()
        
        # Set environment for parent class
        os.environ['SERVICE_ACCOUNT_PATH'] = self.auto_config['service_account_path']
        os.environ['GOOGLE_DRIVE_FOLDER_ID'] = self.auto_config['folder_id']
        
        # Initialize parent
        super().__init__(tool_name="zero_config")
        
        # Override with auto-configured values
        self.folder_id = self.auto_config['folder_id']
        self.notebook_id = self.auto_config['notebook_id']
        
        # Auto-initialize
        self.initialize()
    
    def execute(self, code, timeout=30):
        """Execute code with zero config"""
        return self.execute_code(code, timeout)
    
    def get_notebook_url(self):
        """Get the Colab notebook URL"""
        return self.auto_config['notebook_url']

# Convenience function for one-line usage
def colab_execute(code, service_account_path=None):
    """
    Execute code in Colab with zero configuration.
    
    Example:
        from colab_integration import colab_execute
        result = colab_execute("print('Hello from GPU!')")
        print(result['output'])
    """
    bridge = ZeroConfigBridge(service_account_path)
    return bridge.execute(code)

# For VS Code extension
class VSCodeColabBridge:
    """Special version for VS Code extension with auto-setup"""
    
    def __init__(self):
        self.bridge = None
        self._ensure_setup()
    
    def _ensure_setup(self):
        """Ensure Colab is set up"""
        if not self.bridge:
            print("🚀 Initializing Colab Bridge (one-time setup)...")
            self.bridge = ZeroConfigBridge()
            print("✅ Ready!")
    
    def execute_selection(self, code):
        """Execute selected code"""
        self._ensure_setup()
        
        print("📤 Sending to Colab...")
        result = self.bridge.execute(code)
        
        if result.get('status') == 'success':
            return result.get('output', '')
        elif result.get('status') == 'error':
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        else:
            return "⏳ Processing... (make sure Colab notebook is running)"
    
    def open_notebook(self):
        """Open the Colab notebook"""
        self._ensure_setup()
        url = self.bridge.get_notebook_url()
        print(f"🔗 Notebook URL: {url}")
        return url

if __name__ == "__main__":
    # Demo
    print("🧪 Testing Zero-Config Bridge...")
    
    # Just one line!
    result = colab_execute('''
import sys
print(f"Python: {sys.version}")
print("Hello from Colab with zero config!")
''')
    
    print(f"\n📥 Result: {result}")