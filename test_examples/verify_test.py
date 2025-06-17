
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
