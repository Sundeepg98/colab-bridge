# Test GPU execution in Colab from VS Code
# Select this code and press Ctrl+Shift+C

import sys
print(f"Python version: {sys.version}")
print(f"Running in: {'Google Colab' if 'google.colab' in sys.modules else 'Local'}")

# Test GPU availability
try:
    import torch
    print(f"\nPyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        
        # Simple GPU computation
        x = torch.rand(1000, 1000).cuda()
        y = torch.rand(1000, 1000).cuda()
        z = torch.matmul(x, y)
        print(f"\nGPU computation successful!")
        print(f"Result shape: {z.shape}")
except ImportError:
    print("\nPyTorch not available - trying TensorFlow...")
    try:
        import tensorflow as tf
        print(f"TensorFlow version: {tf.__version__}")
        print(f"GPUs available: {len(tf.config.list_physical_devices('GPU'))}")
    except:
        print("No ML frameworks available")

# Test basic computation
import numpy as np
result = np.random.rand(100, 100).mean()
print(f"\nNumPy computation result: {result:.6f}")

print("\n✅ Test completed!")