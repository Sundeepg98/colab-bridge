#!/usr/bin/env python3
"""
Non-interactive Colab test
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Setup
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.bridge import ClaudeColabBridge

def run_test():
    print("🚀 Running Colab Integration Test")
    print("=" * 50)
    
    # Initialize bridge
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    print(f"✅ Connected to Google Drive")
    print(f"   Folder: {bridge.folder_id}")
    print(f"   Instance: {bridge.instance_id}")
    
    # Test code
    test_code = '''
import sys
import datetime
print(f"🎉 Test from Claude Tools!")
print(f"Time: {datetime.datetime.now()}")
print(f"Python: {sys.version}")

# Quick computation test
import numpy as np
arr = np.random.rand(100, 100)
print(f"✅ NumPy test: sum = {np.sum(arr):.2f}")
'''
    
    print("\n📤 Sending test request...")
    print("⏳ Waiting for Colab to process...")
    
    try:
        result = bridge.execute_code(test_code, timeout=60)
        
        if result.get('status') == 'success':
            print("\n✅ Success! Colab is working!")
            print("\n📋 Output from Colab:")
            print("-" * 40)
            print(result.get('output', 'No output'))
            print("-" * 40)
        elif result.get('status') == 'pending':
            print("\n⏳ Request created and waiting in Drive")
            print(f"   Request ID: {result.get('request_id')}")
            print("\n📝 To process this request:")
            print("   1. Open: https://colab.research.google.com/drive/1X9EaHlau2jZPoQVhCyjk7x8FOvNINeNh")
            print("   2. Click 'Run all' in the notebook")
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            
    except TimeoutError:
        print("\n⏱️ Request timed out after 60s")
        print("📝 The Colab notebook might not be running")
        print("   Open: https://colab.research.google.com/drive/1X9EaHlau2jZPoQVhCyjk7x8FOvNINeNh")
        print("   And click 'Run all'")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    # Check request status
    print("\n📊 Checking Drive for requests...")
    
    try:
        # List files in Drive folder
        query = f"'{bridge.folder_id}' in parents and trashed=false"
        results = bridge.drive_service.files().list(
            q=query,
            fields="files(id, name, createdTime)",
            orderBy="createdTime desc",
            pageSize=10
        ).execute()
        
        files = results.get('files', [])
        if files:
            print(f"\n📁 Found {len(files)} files in Drive:")
            for f in files[:5]:  # Show last 5
                print(f"   - {f['name']}")
        else:
            print("📁 No files found in Drive folder")
            
    except Exception as e:
        print(f"❌ Could not list Drive files: {e}")

if __name__ == "__main__":
    run_test()