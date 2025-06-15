#!/usr/bin/env python3
"""
Test Claude Tools Colab Integration
Run this to verify your setup and send test requests to Colab
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.bridge import ClaudeColabBridge

def main():
    print("🚀 Claude Tools - Colab Integration Test")
    print("=" * 50)
    
    # Check credentials
    sa_path = os.getenv('SERVICE_ACCOUNT_PATH')
    if not sa_path or not os.path.exists(sa_path):
        print("❌ Service account not found!")
        print("   Please check your .env file")
        return
    
    print(f"✅ Using service account: {os.path.basename(sa_path)}")
    
    # Initialize bridge
    try:
        bridge = ClaudeColabBridge()
        bridge.initialize()
        print(f"✅ Connected to Google Drive")
        print(f"   Folder ID: {bridge.folder_id}")
        print(f"   Instance: {bridge.instance_id}")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    print("\n📋 Setup Instructions:")
    print("1. Open Google Colab: https://colab.research.google.com")
    print("2. Upload this notebook: notebooks/colab-processor.ipynb")
    print("3. Run all cells in the notebook")
    print("4. Keep this script running to send test requests")
    
    print("\n⏳ Waiting for you to start the Colab notebook...")
    print("Press Ctrl+C to exit\n")
    
    # Test code
    test_code = '''
import sys
import platform
print(f"🎉 Hello from Colab!")
print(f"Python: {platform.python_version()}")
print(f"System: {platform.system()}")

# Check GPU
try:
    import torch
    if torch.cuda.is_available():
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("❌ No GPU available")
except:
    print("📦 PyTorch not installed")

# Test computation
import numpy as np
arr = np.random.rand(1000, 1000)
result = np.sum(arr)
print(f"✅ NumPy test: sum of 1M random numbers = {result:.2f}")
'''
    
    try:
        while True:
            input("\n📤 Press Enter to send a test request (Ctrl+C to exit)...")
            
            print("⏳ Sending request...")
            start_time = time.time()
            
            try:
                result = bridge.execute_code(test_code, timeout=60)
                
                if result.get('status') == 'success':
                    print(f"\n✅ Success! (took {time.time() - start_time:.1f}s)")
                    print("📋 Output:")
                    print("-" * 40)
                    print(result.get('output', 'No output'))
                    print("-" * 40)
                elif result.get('status') == 'error':
                    print(f"\n❌ Error: {result.get('error')}")
                else:
                    print(f"\n⏱️ Request timed out after {time.time() - start_time:.1f}s")
                    print("   Make sure the Colab notebook is running!")
                    
            except TimeoutError:
                print(f"\n⏱️ Request timed out")
                print("   Make sure the Colab notebook is running!")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")

if __name__ == "__main__":
    main()