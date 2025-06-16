#!/usr/bin/env python3
"""
Test API-based execution with different providers
Shows the power of API-based approach vs browser automation
"""

import os
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

print("🚀 TESTING API-BASED GPU EXECUTION")
print("=" * 60)
print("This demonstrates the API approach - no browser needed!")
print("=" * 60)

# Test the API-based executor
try:
    from colab_integration.api_based_execution import (
        APIBasedGPUExecutor, 
        ZeroConfigAPIBridge,
        VSCodeAPIBridge,
        api_execute
    )
    print("✅ API modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 1: Provider detection
print("\n1️⃣ PROVIDER DETECTION")
print("-" * 40)

executor = APIBasedGPUExecutor()
print(f"🎯 Primary provider: {executor.preferred_provider}")
print(f"📋 Available providers: {list(executor.providers.keys())}")

# Check what's available
providers_status = {}
for name, provider in executor.providers.items():
    try:
        if name == 'runpod':
            available = bool(os.getenv('RUNPOD_API_KEY'))
            reason = "API key set" if available else "RUNPOD_API_KEY not set"
        elif name == 'modal':
            available = bool(os.getenv('MODAL_TOKEN'))
            reason = "Token set" if available else "MODAL_TOKEN not set"
        elif name == 'replicate':
            available = bool(os.getenv('REPLICATE_API_TOKEN'))
            reason = "Token set" if available else "REPLICATE_API_TOKEN not set"
        elif name == 'local':
            available = True
            reason = "Always available"
        else:
            available = False
            reason = "Unknown provider"
        
        providers_status[name] = {'available': available, 'reason': reason}
        status_icon = "✅" if available else "❌"
        print(f"   {status_icon} {name}: {reason}")
        
    except Exception as e:
        providers_status[name] = {'available': False, 'reason': str(e)}
        print(f"   ❌ {name}: {e}")

# Test 2: Simple execution
print("\n2️⃣ SIMPLE EXECUTION TEST")
print("-" * 40)

simple_code = '''
import sys
print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
print("✅ Basic execution successful!")
'''

try:
    print("📤 Executing simple code...")
    result = api_execute(simple_code)
    
    print(f"   Status: {result['status']}")
    print(f"   Provider: {result.get('provider', 'unknown')}")
    print(f"   GPU Used: {result.get('gpu_used', False)}")
    print(f"   Output:")
    for line in result.get('output', '').strip().split('\n'):
        print(f"     {line}")
        
except Exception as e:
    print(f"❌ Simple execution failed: {e}")

# Test 3: VS Code simulation
print("\n3️⃣ VS CODE EXTENSION SIMULATION")
print("-" * 40)

try:
    vscode_bridge = VSCodeAPIBridge()
    
    # Simulate user selecting code and pressing Ctrl+Shift+C
    selected_code = '''
# User selected this code in VS Code
import math
result = math.sqrt(42)
print(f"Square root of 42: {result:.3f}")

# Check compute environment
import platform
print(f"Platform: {platform.system()}")
print(f"Architecture: {platform.machine()}")
'''
    
    print("🎯 Simulating VS Code extension:")
    print("   User selects code and presses Ctrl+Shift+C...")
    
    output = vscode_bridge.execute_selection(selected_code)
    print(f"\n📺 VS Code would show:")
    print("=" * 40)
    print(output)
    print("=" * 40)
    
except Exception as e:
    print(f"❌ VS Code simulation failed: {e}")

# Test 4: Configuration check
print("\n4️⃣ CONFIGURATION STATUS")
print("-" * 40)

try:
    vscode_bridge = VSCodeAPIBridge()
    config = vscode_bridge.configure()
    
    print(f"🔧 Configuration:")
    print(f"   Available providers: {config['available_providers']}")
    print(f"   Current provider: {config['current_provider']}")
    
    if config['setup_required']:
        print(f"\n⚙️  Optional setup for GPU access:")
        for item in config['setup_required']:
            print(f"     • {item}")
    else:
        print(f"\n✅ All GPU providers configured!")
        
except Exception as e:
    print(f"❌ Configuration check failed: {e}")

# Test 5: Package detection
print("\n5️⃣ PACKAGE DETECTION TEST")
print("-" * 40)

gpu_code = '''
# This code would benefit from GPU
import torch
import numpy as np

# Create tensors
x = torch.randn(100, 100)
y = torch.randn(100, 100)

# Matrix multiplication
z = torch.matmul(x, y)
print(f"Tensor shape: {z.shape}")

# NumPy equivalent
a = np.random.randn(100, 100)
b = np.random.randn(100, 100)
c = np.matmul(a, b)
print(f"Array shape: {c.shape}")

print("✅ GPU-ready code executed!")
'''

try:
    bridge = ZeroConfigAPIBridge()
    detected_packages = bridge._detect_packages(gpu_code)
    
    print(f"🔍 Auto-detected packages: {detected_packages}")
    print(f"📤 Would execute with these packages...")
    
    # Don't actually execute GPU code without proper setup
    print(f"💡 This would use {bridge.executor.preferred_provider} provider")
    
except Exception as e:
    print(f"❌ Package detection failed: {e}")

# Summary
print("\n" + "=" * 60)
print("📊 API-BASED APPROACH SUMMARY")
print("=" * 60)

available_count = sum(1 for p in providers_status.values() if p['available'])
total_count = len(providers_status)

print(f"\n✅ Working providers: {available_count}/{total_count}")
print(f"🎯 Primary provider: {executor.preferred_provider}")
print(f"🔄 Fallback available: {'✅ Yes' if available_count > 1 else '❌ Local only'}")

print(f"\n💡 Key advantages over browser automation:")
print(f"   ✅ No browser dependencies")
print(f"   ✅ No manual notebook setup")
print(f"   ✅ Direct API calls - faster & more reliable")
print(f"   ✅ Multiple provider support")
print(f"   ✅ Automatic fallbacks")
print(f"   ✅ Works in any environment")

print(f"\n🚀 Ready for VS Code extension:")
print(f"   1. User installs extension")
print(f"   2. Optionally adds GPU API keys")
print(f"   3. Presses Ctrl+Shift+C")
print(f"   4. Code executes on best available provider")
print(f"   5. Results appear in VS Code")

print(f"\n🎯 This is the RIGHT way to build it!")
print(f"   No Playwright, no browser automation, just clean APIs!")