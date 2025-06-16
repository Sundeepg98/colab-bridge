#!/usr/bin/env python3
"""
INSTANT TEST - No setup required!
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("⚡ INSTANT COLAB-BRIDGE TEST")
print("=" * 50)

# Set environment
os.environ['SERVICE_ACCOUNT_PATH'] = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
os.environ['GOOGLE_DRIVE_FOLDER_ID'] = '1ruRdOXUJi16sHgDtpgxqtR7A7g7J8PpA'

from colab_integration.bridge import ClaudeColabBridge

bridge = ClaudeColabBridge()
bridge.initialize()

print(f"✅ Bridge ready!")

# Quick test
test_code = '''
print("🔥 INSTANT TEST RESULT!")
import sys
print(f"Python: {sys.version}")
try:
    import torch
    print(f"GPU: {torch.cuda.is_available()}")
except:
    print("PyTorch not available")
print("✅ Colab execution working!")
'''

print("\n📤 Sending test code...")
print("⏰ IF NOTEBOOK IS RUNNING, you'll see results in 10 seconds...")

try:
    result = bridge.execute_code(test_code, timeout=30)
    if result and result.get('status') == 'success':
        print("\n🎉 SUCCESS! COLAB IS WORKING!")
        print(result.get('output'))
    else:
        print("\n⚠️ No response - Please run the notebook first")
        print("🔗 https://colab.research.google.com/drive/1tWRrTlG_rBLdUb9Vs16i9DURsJiluN_Z")
except:
    print("\n💡 Start the notebook and try again")