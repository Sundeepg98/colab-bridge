#!/usr/bin/env python3
"""
Upload and create shareable auto-run Colab notebook
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.auto_colab import AutoColabManager
from colab_integration.full_auto import FullyAutomatedColab

def main():
    print("🚀 Uploading Auto-Run Notebook to Google Drive")
    print("=" * 50)
    
    # Initialize
    auto = FullyAutomatedColab(
        service_account_path=os.getenv('SERVICE_ACCOUNT_PATH'),
        drive_folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    )
    
    auto.initialize()
    
    # Create and upload zero-click notebook
    notebook_path = auto.create_colab_api_notebook()
    result = auto.upload_and_get_link(notebook_path)
    
    print("\n✅ Auto-Run Notebook Uploaded!")
    print("\n🔗 Shareable Links:")
    print(f"Standard: {result['colab_link']}")
    print(f"Auto-run: {result['auto_run_link']}")
    
    # Test the integration
    print("\n🧪 Testing the setup...")
    from colab_integration.bridge import ClaudeColabBridge
    
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    # Send a test request
    test_code = '''
print("🎯 Auto-execution test successful!")
print("The notebook is processing Claude Tools requests automatically")
'''
    
    result = bridge.execute_code(test_code, timeout=10)
    print(f"\n📊 Test request created: {result.get('request_id', 'pending')}")
    
    print("\n✅ Setup Complete!")
    print("\n📝 To use:")
    print(f"1. Open: {result.get('auto_run_link', result['colab_link'])}")
    print("2. The notebook will start automatically")
    print("3. Grant Drive access when prompted")
    print("4. That's it - fully automated!")

if __name__ == "__main__":
    main()