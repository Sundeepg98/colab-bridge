#!/usr/bin/env python3
"""Test Colab Bridge directly without VS Code extension"""

import sys
import os

# Add colab-bridge to Python path
sys.path.insert(0, '/var/projects/colab-bridge')

print("🧪 Testing Colab Bridge Direct Execution")
print("=" * 50)

try:
    # Import the bridge
    from colab_integration.universal_bridge import UniversalColabBridge
    
    # Create bridge instance
    print("\n1️⃣ Creating Colab Bridge instance...")
    bridge = UniversalColabBridge(tool_name='test')
    
    # Set up credentials if needed
    os.environ['SERVICE_ACCOUNT_PATH'] = '/var/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
    os.environ['GOOGLE_DRIVE_FOLDER_ID'] = '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z'
    
    # Change to colab-bridge directory for relative paths
    os.chdir('/var/projects/colab-bridge')
    
    # Initialize
    print("2️⃣ Initializing bridge...")
    bridge.initialize()
    print("✅ Bridge initialized successfully")
    
    # Read the GPU test file
    print("\n3️⃣ Reading test_gpu.py...")
    with open('/tmp/colab-bridge-automated-test/test_gpu.py', 'r') as f:
        gpu_test_code = f.read()
    
    print("Code to execute:")
    print("-" * 40)
    print(gpu_test_code)
    print("-" * 40)
    
    # Execute the code
    print("\n4️⃣ Executing on Colab...")
    result = bridge.execute_code(gpu_test_code, timeout=30)
    
    # Show results
    print("\n5️⃣ Results:")
    print(f"Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        print("\n✅ SUCCESS! Output from Colab:")
        print("-" * 40)
        print(result.get('output', 'No output'))
        print("-" * 40)
    elif result.get('status') == 'error':
        print("\n❌ ERROR:")
        print(result.get('error', 'Unknown error'))
    else:
        print("\n⏳ PENDING:")
        print(f"Request ID: {result.get('request_id')}")
        print("Make sure the Colab notebook processor is running!")
        print("\nTo run the processor:")
        print("1. Open: https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA")
        print("2. Run all cells in the notebook")
        print("3. Keep it running and try this script again")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
print("\n" + "=" * 50)
print("Test complete!")