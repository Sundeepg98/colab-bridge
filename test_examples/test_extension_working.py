#!/usr/bin/env python3
"""Test if the VS Code extension can execute code on Colab"""

# This script tests if the colab-bridge extension is working
# When run through VS Code with the extension, it should execute on Colab

import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Check if running on Colab
try:
    import google.colab
    print("✅ SUCCESS: Running on Google Colab!")
    print("The VS Code extension is working correctly!")
    
    # Try GPU test
    try:
        import torch
        print(f"\nPyTorch available: ✅")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    except:
        print("\nPyTorch not available in this environment")
        
except ImportError:
    print("❌ ERROR: Running locally (not on Colab)")
    print("The VS Code extension is NOT redirecting to Colab")
    print("\nTroubleshooting:")
    print("1. Make sure VS Code extension is installed")
    print("2. Check if extension is activated")
    print("3. Try: Ctrl+Shift+P -> 'Colab Bridge: Execute File in Colab'")