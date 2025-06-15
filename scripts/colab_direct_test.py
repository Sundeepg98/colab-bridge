#!/usr/bin/env python3
"""
Direct Colab Integration Test
Tests Claude Tools by uploading and running notebooks in Google Colab
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Add parent to path and load env
sys.path.insert(0, str(Path(__file__).parent.parent))
load_dotenv(Path(__file__).parent.parent / '.env')

from colab_integration.bridge import ClaudeColabBridge

def test_colab_direct():
    """Test direct Colab integration"""
    print("🚀 Testing Direct Colab Integration")
    print("=" * 50)
    
    # Initialize bridge
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    print(f"\n✅ Connected to Google Drive")
    print(f"   Folder ID: {bridge.folder_id}")
    print(f"   Instance: {bridge.instance_id}")
    
    # Create a test request
    print("\n📝 Creating test request...")
    test_code = """
import sys
print(f"Python version: {sys.version}")
print("Testing Claude Tools integration!")

# Check if we're in Colab
try:
    import google.colab
    print("✅ Running in Google Colab!")
except ImportError:
    print("❌ Not in Colab environment")

# Test GPU availability
import torch
if torch.cuda.is_available():
    print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
else:
    print("❌ No GPU available")
"""
    
    request_data = {
        "type": "execute_code",
        "code": test_code,
        "timestamp": time.time()
    }
    
    # Execute code through bridge
    print("📤 Sending code execution request...")
    result = bridge.execute_code(test_code)
    
    if 'request_id' in result:
        print(f"✅ Request created: {result['request_id']}")
        
        print("\n📋 Instructions for Colab:")
        print("1. Open Google Colab: https://colab.research.google.com")
        print("2. Upload the notebook: notebooks/colab-processor.ipynb")
        print("3. Mount your Google Drive when prompted")
        print("4. Run all cells in the notebook")
        print("5. The notebook will process this request automatically")
        
        print(f"\n🔍 Request is waiting in Drive folder: {bridge.folder_id}")
        print("⏳ Once Colab is running, it will process the request...")
    else:
        print("\n📋 Result:")
        if result.get('status') == 'pending':
            print("⏳ Request queued. Start the Colab notebook to process it.")
        elif result.get('status') == 'success':
            print(f"✅ Output:\n{result.get('output', 'No output')}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")

def check_colab_apis():
    """Check what Google Cloud APIs might be needed"""
    print("\n🔍 Checking Google Cloud API requirements:")
    print("=" * 50)
    
    # Check service account permissions
    sa_path = os.getenv('SERVICE_ACCOUNT_PATH')
    if sa_path and os.path.exists(sa_path):
        with open(sa_path, 'r') as f:
            sa_data = json.load(f)
            
        print(f"✅ Service Account: {sa_data.get('client_email', 'Unknown')}")
        print(f"✅ Project ID: {sa_data.get('project_id', 'Unknown')}")
        
        print("\n📋 Required Google Cloud APIs:")
        print("1. Google Drive API - For file operations (Already using)")
        print("2. Google Sheets API - Optional, for data exchange")
        print("3. Google Cloud Storage - Optional, for large files")
        
        print("\n✅ Current setup uses only Google Drive API")
        print("   No additional API keys needed for basic Colab integration")
        
        print("\n💡 Optional enhancements:")
        print("- Colab Pro: For longer runtime and better GPUs")
        print("- Google Cloud Storage: For model/dataset storage")
        print("- Vertex AI: For managed ML workflows")
    else:
        print("❌ No service account found")

if __name__ == "__main__":
    test_colab_direct()
    check_colab_apis()