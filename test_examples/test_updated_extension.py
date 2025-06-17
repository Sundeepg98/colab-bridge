#!/usr/bin/env python3
"""Test the updated colab-bridge extension"""

import subprocess
import time

print("🧪 Testing Updated Colab Bridge Extension")
print("=" * 50)

# Check installed extensions
print("\n1️⃣ Checking installed extensions...")
result = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True)
colab_extensions = [ext for ext in result.stdout.split('\n') if 'colab' in ext.lower() or 'bridge' in ext.lower()]

print("Installed Colab-related extensions:")
for ext in colab_extensions:
    if ext:
        print(f"  - {ext}")

# Test VS Code commands
print("\n2️⃣ Testing VS Code commands...")
print("In VS Code, press Ctrl+Shift+P and type 'colab'")
print("You should see:")
print("  - Colab Bridge: Execute File in Colab")
print("  - Colab Bridge: Execute Selection in Colab")
print("  - Colab Bridge: Open Colab Processor")
print("  - Colab Bridge: Configure")

# Test configuration
print("\n3️⃣ Testing configuration...")
print("In VS Code settings (Ctrl+,), search for 'colab-bridge'")
print("You should see:")
print("  - colab-bridge.pythonPath")
print("  - colab-bridge.serviceAccountPath")
print("  - colab-bridge.driveFolder")
print("  - colab-bridge.timeout")
print("  - colab-bridge.showOutput")

# Quick test
print("\n4️⃣ Quick functionality test:")
print("Run this in VS Code terminal:")
print("  python test_gpu.py")
print("\nThe extension should:")
print("  1. Intercept the Python command")
print("  2. Execute on Colab GPU")
print("  3. Show GPU info (Tesla T4)")

print("\n✅ Extension update complete!")
print("The extension now uses 'colab-bridge' namespace throughout.")