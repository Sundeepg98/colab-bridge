#!/usr/bin/env python3
"""
Test Claude Tools with your live credentials
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add to path and load env
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

from colab_integration.bridge import ClaudeColabBridge

print("🧪 Testing Claude Tools with your credentials")
print("=" * 50)

# Initialize bridge
bridge = ClaudeColabBridge()
bridge.initialize()

print(f"\n✅ Successfully connected with:")
print(f"   Service Account: {os.path.basename(bridge.config.get('service_account_path', 'N/A'))}")
print(f"   Drive Folder ID: {bridge.folder_id}")
print(f"   Instance ID: {bridge.instance_id}")

print("\n📝 To complete the test:")
print("1. Open Google Colab")
print("2. Upload notebooks/basic-integration.ipynb")
print("3. Run all cells in the notebook")
print("4. Then run this script again")

print("\n🚀 Once Colab is running, you can execute code like:")
print("""
result = bridge.execute_code('''
import numpy as np
import pandas as pd
print("Hello from Colab!")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
''')
print(result['output'])
""")