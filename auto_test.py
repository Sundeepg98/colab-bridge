#!/usr/bin/env python3
"""
Fully Automated Claude Tools Test
Handles Colab setup and testing automatically
"""

import os
import sys
import time
import threading
from pathlib import Path
from dotenv import load_dotenv

# Setup
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.bridge import ClaudeColabBridge
from colab_integration.auto_colab import AutoColabManager

def auto_test():
    """Run fully automated test"""
    print("🤖 Claude Tools - Fully Automated Test")
    print("=" * 50)
    
    # Step 1: Setup Colab automatically
    print("\n📋 Step 1: Setting up Colab notebook...")
    
    manager = AutoColabManager(
        service_account_path=os.getenv('SERVICE_ACCOUNT_PATH'),
        drive_folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    )
    
    manager.initialize()
    result = manager.start_colab_session(open_browser=True)
    
    print("\n⏳ Waiting 10 seconds for Colab to start...")
    time.sleep(10)
    
    # Step 2: Initialize bridge
    print("\n📋 Step 2: Initializing Claude Tools bridge...")
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    # Step 3: Send test requests
    print("\n📋 Step 3: Sending test requests...")
    
    test_codes = [
        {
            "name": "Basic Test",
            "code": '''
print("🎉 Hello from automated Colab!")
import platform
print(f"Python: {platform.python_version()}")
print(f"System: {platform.system()}")
'''
        },
        {
            "name": "GPU Test", 
            "code": '''
import torch
if torch.cuda.is_available():
    print(f"✅ GPU Available: {torch.cuda.get_device_name(0)}")
    print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("❌ No GPU available")
'''
        },
        {
            "name": "ML Libraries Test",
            "code": '''
import numpy as np
import pandas as pd
import matplotlib
import sklearn
print(f"✅ NumPy: {np.__version__}")
print(f"✅ Pandas: {pd.__version__}")
print(f"✅ Matplotlib: {matplotlib.__version__}")
print(f"✅ Scikit-learn: {sklearn.__version__}")
'''
        }
    ]
    
    for test in test_codes:
        print(f"\n🧪 Running: {test['name']}")
        print("⏳ Sending request...")
        
        try:
            start_time = time.time()
            result = bridge.execute_code(test['code'], timeout=60)
            
            if result.get('status') == 'success':
                elapsed = time.time() - start_time
                print(f"✅ Success! (took {elapsed:.1f}s)")
                print("📋 Output:")
                print("-" * 40)
                print(result.get('output', 'No output'))
                print("-" * 40)
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                
        except TimeoutError:
            print("⏱️ Request timed out - Colab might still be starting")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(2)  # Brief pause between tests
    
    print("\n✅ Automated test complete!")
    print("\n📝 Next steps:")
    print("1. The Colab notebook is running and processing requests")
    print("2. You can now use bridge.execute_code() to run any Python code")
    print("3. The notebook will continue running for 1 hour")

def monitor_colab(bridge, duration=300):
    """Monitor Colab status in background"""
    print(f"\n📊 Monitoring Colab for {duration/60:.0f} minutes...")
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            # Send heartbeat
            result = bridge.execute_code('print("heartbeat")', timeout=10)
            if result.get('status') == 'success':
                print("💚 Colab is responsive", end='\r')
            else:
                print("💛 Colab not responding", end='\r')
        except:
            print("💔 Colab disconnected", end='\r')
        
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    auto_test()
    
    # Optional: Continue monitoring
    print("\n🔄 Starting background monitor...")
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    monitor_thread = threading.Thread(target=monitor_colab, args=(bridge, 300))
    monitor_thread.daemon = True
    monitor_thread.start()
    
    try:
        print("Press Ctrl+C to exit monitor\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")