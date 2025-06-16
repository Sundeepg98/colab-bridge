#!/usr/bin/env python3
"""
Test the hybrid processor specifically
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.bridge import ClaudeColabBridge

def test_hybrid():
    print("🧪 Testing Hybrid Processor")
    print("=" * 50)
    
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    # Create a test that will show clear output
    test_code = '''
print("🎉 SUCCESS! Hybrid processor is working!")
print("=" * 50)

import datetime
import platform
import sys

print(f"⏰ Processed at: {datetime.datetime.now()}")
print(f"🐍 Python: {platform.python_version()}")
print(f"🖥️  System: {platform.system()}")

# Test some computation
import numpy as np
arr = np.random.rand(1000)
mean_val = np.mean(arr)
std_val = np.std(arr)

print(f"🔢 Random array mean: {mean_val:.4f}")
print(f"📊 Random array std: {std_val:.4f}")

# Test GPU if available
try:
    import torch
    if torch.cuda.is_available():
        device = torch.cuda.get_device_name(0)
        memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"🚀 GPU: {device}")
        print(f"💾 Memory: {memory:.1f} GB")
    else:
        print("💻 CPU only (no GPU)")
except ImportError:
    print("📦 PyTorch not available")

print("=" * 50)
print("✅ Test completed successfully!")
'''
    
    print("📤 Sending test to hybrid processor...")
    print("\n📋 Expected result if processor is running:")
    print("- Request gets processed automatically")
    print("- Response appears in Drive folder")
    print("- Shows Python/system info and computations")
    
    try:
        result = bridge.execute_code(test_code, timeout=30)
        
        if result.get('status') == 'success':
            print("\n🎉 HYBRID PROCESSOR IS RUNNING!")
            print("📋 Output:")
            print("-" * 50)
            print(result.get('output'))
            print("-" * 50)
        else:
            print(f"\n📋 Request queued (ID: {result.get('request_id', 'pending')})")
            print("\n🔗 To start the hybrid processor:")
            print("   https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA")
            print("\n📝 It will:")
            print("   1. Auto-run when you open it")
            print("   2. Process this test request")
            print("   3. Show debug cells for monitoring")
            
    except Exception as e:
        print(f"\n⏱️ Request created but timed out: {e}")
        print("\n🔗 Start the hybrid processor:")
        print("   https://colab.research.google.com/drive/1XhtEroHqX5Y8hetP-xCN_FMF-Ea81tAA")

if __name__ == "__main__":
    test_hybrid()