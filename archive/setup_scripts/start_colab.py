#!/usr/bin/env python3
"""
One-Click Colab Starter for Claude Tools
Just run: python3 start_colab.py
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Setup
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.auto_colab import AutoColabManager

def main():
    print("🚀 Claude Tools - One-Click Colab Starter")
    print("=" * 50)
    
    # Check environment
    sa_path = os.getenv('SERVICE_ACCOUNT_PATH')
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    if not sa_path or not folder_id:
        print("❌ Missing configuration in .env file")
        return
    
    print("✅ Configuration loaded")
    print(f"   Service Account: {Path(sa_path).name}")
    print(f"   Drive Folder: {folder_id}")
    
    # Initialize manager
    print("\n🔧 Initializing...")
    manager = AutoColabManager(sa_path, folder_id)
    manager.initialize()
    
    # Create and upload notebook
    print("\n📤 Creating and uploading Colab notebook...")
    result = manager.start_colab_session(open_browser=True)
    
    print("\n✅ Colab notebook is ready!")
    print("📋 What happens next:")
    print("1. ✅ Browser opened with Colab notebook")
    print("2. ⏳ Click 'Run all' or Ctrl+F9 in Colab")
    print("3. ✅ Allow Drive access when prompted")
    print("4. 🤖 Notebook will auto-process requests")
    
    print("\n⏳ Waiting 20 seconds for Colab to initialize...")
    for i in range(20, 0, -1):
        print(f"   {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\n\n✅ Colab should now be running!")
    print("\n📝 Test it with:")
    print("   python3 test_colab_integration.py")
    print("\nOr use in your code:")
    print("   from colab_integration.bridge import ClaudeColabBridge")
    print("   bridge = ClaudeColabBridge()")
    print("   bridge.initialize()")
    print("   result = bridge.execute_code('print(\"Hello from Colab!\")')")
    
    # Optional: Run test automatically
    response = input("\n🧪 Run a test now? (y/n): ")
    if response.lower() == 'y':
        print("\n🧪 Running test...")
        from colab_integration.bridge import ClaudeColabBridge
        
        bridge = ClaudeColabBridge()
        bridge.initialize()
        
        test_code = '''
import sys
print("🎉 Colab is working!")
print(f"Python {sys.version}")
print("Ready for Claude Tools requests!")
'''
        
        try:
            result = bridge.execute_code(test_code, timeout=30)
            if result.get('status') == 'success':
                print("\n✅ Test successful!")
                print("Output:")
                print(result.get('output'))
            else:
                print(f"\n❌ Test failed: {result.get('error')}")
        except TimeoutError:
            print("\n⏱️ Test timed out - make sure you clicked 'Run all' in Colab")
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()