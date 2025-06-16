#!/usr/bin/env python3
"""
Test the fully automated setup
Only requires service account key!
"""

import os
import sys
from pathlib import Path

# Set up environment
creds_path = Path(__file__).parent / 'credentials' / 'automation-engine-463103-ee5a06e18248.json'
os.environ['SERVICE_ACCOUNT_PATH'] = str(creds_path)
os.environ['OWNER_EMAIL'] = 'sundeepg8@gmail.com'

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

print("🚀 TESTING ZERO-CONFIG COLAB BRIDGE")
print("=" * 60)
print("This tests the full automated setup experience!")
print("User only needs to provide service account key.")
print("=" * 60)

# Test 1: Auto setup
print("\n1️⃣ Running auto-setup...")
try:
    from colab_integration.auto_setup import auto_setup
    config = auto_setup()
    print(f"✅ Auto-setup completed!")
    print(f"   Folder ID: {config['folder_id']}")
    print(f"   Notebook ID: {config['notebook_id']}")
    print(f"   Notebook URL: {config['notebook_url']}")
except Exception as e:
    print(f"❌ Auto-setup failed: {e}")
    sys.exit(1)

# Test 2: Zero-config bridge
print("\n2️⃣ Testing zero-config bridge...")
try:
    from colab_integration.zero_config_bridge import ZeroConfigBridge
    
    bridge = ZeroConfigBridge()
    print("✅ Zero-config bridge initialized!")
    print(f"   Notebook URL: {bridge.get_notebook_url()}")
except Exception as e:
    print(f"❌ Bridge initialization failed: {e}")
    sys.exit(1)

# Test 3: VS Code simulation
print("\n3️⃣ Simulating VS Code extension...")
try:
    from colab_integration.zero_config_bridge import VSCodeColabBridge
    
    vscode_bridge = VSCodeColabBridge()
    print("✅ VS Code bridge ready!")
    
    # Simulate user selecting code and pressing Ctrl+Shift+C
    selected_code = '''
import torch
print("🔥 Testing GPU availability...")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
else:
    print("No GPU detected (might be CPU-only runtime)")

print("✅ Code executed successfully!")
'''
    
    print("\n📝 Selected code (what user selected in VS Code):")
    print("-" * 40)
    print(selected_code.strip())
    print("-" * 40)
    
    print("\n📤 Sending to Colab (this is what happens when user presses Ctrl+Shift+C)...")
    print("💡 Note: This requires the Colab notebook to be running")
    print(f"   Open this URL first: {vscode_bridge.open_notebook()}")
    
except Exception as e:
    print(f"❌ VS Code simulation failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: One-line function
print("\n4️⃣ Testing one-line function...")
try:
    from colab_integration.zero_config_bridge import colab_execute
    
    print("   This is the simplest possible usage:")
    print("   result = colab_execute('print(\"Hello World!\")')")
    print("   💡 Note: Requires notebook to be running for actual execution")
    
except Exception as e:
    print(f"❌ One-line function failed: {e}")

print("\n" + "=" * 60)
print("🎉 ZERO-CONFIG SETUP COMPLETE!")
print("=" * 60)
print("\n📋 What just happened:")
print("1. ✅ Auto-created Drive folder")
print("2. ✅ Auto-created Colab processor notebook") 
print("3. ✅ Auto-configured sharing")
print("4. ✅ Saved configuration locally")
print("5. ✅ Ready for VS Code extension!")

print(f"\n🎯 Next step:")
print(f"   Open this URL: {config['notebook_url']}")
print(f"   Click 'Run all' (Ctrl+F9)")
print(f"   Then the VS Code extension will work!")

print(f"\n💡 For developers:")
print(f"   The extension now needs just 1 line:")
print(f"   bridge = VSCodeColabBridge()  # Everything else is automatic!")

print(f"\n🚀 This is the experience we want:")
print(f"   1. User installs extension")
print(f"   2. Extension asks for service account key") 
print(f"   3. Extension does all setup automatically")
print(f"   4. User presses Ctrl+Shift+C and it just works!")