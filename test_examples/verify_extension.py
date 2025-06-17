#!/usr/bin/env python3
"""Verify the colab-bridge extension is actually working"""

import subprocess
import json
import os
import time

def verify_extension():
    """Verify the extension is properly configured and working"""
    
    print("🔍 Verifying Colab Bridge Extension")
    print("=" * 50)
    
    # 1. Check VS Code workspace settings
    print("\n1️⃣ Checking workspace settings...")
    workspace_file = "/tmp/colab-bridge-automated-test/test.code-workspace"
    
    if os.path.exists(workspace_file):
        with open(workspace_file, 'r') as f:
            settings = json.load(f)
            print(f"Workspace settings found:")
            for key, value in settings.get('settings', {}).items():
                print(f"  {key}: {value}")
    
    # 2. Check if .vscode/settings.json exists
    vscode_settings = "/tmp/colab-bridge-automated-test/.vscode/settings.json"
    if os.path.exists(vscode_settings):
        print(f"\n✅ VS Code settings found: {vscode_settings}")
        with open(vscode_settings, 'r') as f:
            settings = json.load(f)
            print(json.dumps(settings, indent=2))
    else:
        print("\n❌ No .vscode/settings.json found")
    
    # 3. Test Python execution
    print("\n2️⃣ Testing Python execution...")
    test_code = """
import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Check if running on Colab
try:
    import google.colab
    print("✅ Running on Google Colab!")
except ImportError:
    print("❌ Running locally (not on Colab)")

# Check GPU
try:
    import torch
    if torch.cuda.is_available():
        print(f"✅ GPU available: {torch.cuda.get_device_name(0)}")
    else:
        print("❌ No GPU available")
except ImportError:
    print("❌ PyTorch not installed")
"""
    
    with open("/tmp/colab-bridge-automated-test/verify_test.py", "w") as f:
        f.write(test_code)
    
    print("Created verify_test.py")
    
    # 4. Check extension commands availability
    print("\n3️⃣ Checking extension commands...")
    
    # Try to get extension info
    result = subprocess.run(
        ["code", "--list-extensions", "--show-versions"], 
        capture_output=True, 
        text=True
    )
    
    colab_ext = [line for line in result.stdout.split('\n') if 'colab-bridge' in line]
    if colab_ext:
        print(f"✅ Extension installed: {colab_ext[0]}")
    else:
        print("❌ Colab Bridge extension not found")
    
    # 5. Create a test to run in VS Code
    print("\n4️⃣ Manual verification steps:")
    print("1. Open VS Code in the test workspace:")
    print(f"   code {os.getcwd()}")
    print("\n2. Open the integrated terminal (Ctrl+`)")
    print("\n3. Run: python verify_test.py")
    print("\n4. Check the output:")
    print("   - Should show Colab Python path (not local)")
    print("   - Should show 'Running on Google Colab!'")
    print("   - Should show GPU info")
    
    print("\n5. Check status bar (bottom of VS Code):")
    print("   - Should show '☁ Colab GPU: Connected' or similar")
    
    print("\n6. Try VS Code commands (Ctrl+Shift+P):")
    print("   - Type 'colab' to see available commands")
    print("   - Should see 'Colab Bridge:' prefixed commands")
    
    return True

def check_python_module():
    """Check if colab_bridge Python module is working"""
    print("\n5️⃣ Checking Python module...")
    
    try:
        import colab_bridge
        print(f"✅ colab_bridge module found: {colab_bridge.__file__}")
        
        # Check version
        if hasattr(colab_bridge, '__version__'):
            print(f"   Version: {colab_bridge.__version__}")
        
        # Check if bridge can be created
        from colab_integration import UniversalColabBridge
        bridge = UniversalColabBridge()
        print("✅ UniversalColabBridge instance created")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_extension()
    check_python_module()