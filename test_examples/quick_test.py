#!/usr/bin/env python3
"""Quick test to check if Colab Bridge is working"""

import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

# Check if we're running on Colab
try:
    import google.colab
    print("✅ Running on Google Colab!")
except ImportError:
    print("❌ Running locally (not on Colab)")

# Simple GPU test
try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
except ImportError:
    print("PyTorch not available")