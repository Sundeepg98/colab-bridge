
# Simple test for Colab Bridge
print("Testing Colab Bridge...")

# This should execute on Colab GPU
import platform
print(f"Platform: {platform.platform()}")
print(f"Node: {platform.node()}")

# Check for GPU
try:
    import torch
    print(f"GPU Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
except:
    print("PyTorch not available")

print("Test complete!")
