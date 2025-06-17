#!/bin/bash

echo "🚀 Running GPU Test on Colab"
echo "============================"
echo ""

# Method 1: Using VS Code
echo "Method 1: Using VS Code Extension"
echo "---------------------------------"
echo "1. Open VS Code: code /tmp/colab-bridge-automated-test"
echo "2. Open test_gpu.py"
echo "3. Press Ctrl+Shift+Alt+C to run entire file on Colab"
echo "   OR"
echo "   Press Ctrl+Shift+P and type: Colab Bridge: Execute File in Colab"
echo ""

# Method 2: Direct Python
echo "Method 2: Using Python directly"
echo "-------------------------------"
cat << 'EOF' > /tmp/test_colab_gpu.py
import os
import sys
sys.path.insert(0, '/var/projects/colab-bridge')

from colab_integration.universal_bridge import UniversalColabBridge

# Set credentials
os.environ['SERVICE_ACCOUNT_PATH'] = '/var/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
os.environ['GOOGLE_DRIVE_FOLDER_ID'] = '1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z'

# Create and initialize bridge
bridge = UniversalColabBridge(tool_name='gpu_test')
bridge.initialize()

# Read GPU test code
with open('/tmp/colab-bridge-automated-test/test_gpu.py', 'r') as f:
    code = f.read()

# Execute on Colab
print("Executing on Colab GPU...")
result = bridge.execute_code(code, timeout=60)

if result.get('status') == 'success':
    print("\n✅ Success! Output from Colab GPU:")
    print(result.get('output'))
elif result.get('status') == 'error':
    print(f"\n❌ Error: {result.get('error')}")
else:
    print(f"\n⏳ Pending: {result.get('message')}")
    print("Make sure Colab notebook is running!")
EOF

echo "Run: python3 /tmp/test_colab_gpu.py"
echo ""

# Method 3: Command line
echo "Method 3: Using colab-bridge CLI"
echo "---------------------------------"
echo "cd /tmp/colab-bridge-automated-test"
echo "colab-bridge execute --file test_gpu.py"
echo ""

echo "Note: Make sure the Colab processor notebook is running!"
echo "Open: https://colab.research.google.com"