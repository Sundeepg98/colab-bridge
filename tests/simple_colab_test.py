#!/usr/bin/env python3
"""
Simple test to verify Colab connectivity and see what happens
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def test_basic_colab():
    """Test basic Colab functionality"""
    print("🧪 BASIC COLAB TEST")
    print("=" * 30)
    
    try:
        bridge = UniversalColabBridge("basic_test")
        bridge.initialize()
        print("✅ Connected to Google Colab backend")
        
        # Test 1: Simple print
        print("\n📋 Test 1: Simple execution")
        result1 = bridge.execute_code("print('Hello from Colab!')", timeout=15)
        
        print(f"Status: {result1.get('status')}")
        if result1.get('status') == 'success':
            print(f"Output: {result1.get('output')}")
            print("✅ Basic execution works!")
            
            # Test 2: Check Python environment
            print("\n📋 Test 2: Python environment")
            result2 = bridge.execute_code("""
import sys
print(f"Python: {sys.version[:20]}")
print("✅ Python is working")

# Check if we're in Colab
try:
    import google.colab
    print("✅ This is Google Colab")
except ImportError:
    print("❌ Not in Colab environment")
""", timeout=15)
            
            print(f"Status: {result2.get('status')}")
            if result2.get('status') == 'success':
                print(f"Output: {result2.get('output')}")
                return True
            else:
                print(f"Error: {result2.get('error')}")
                return False
        
        elif result1.get('status') == 'queued':
            print("⏳ Commands are being queued")
            print("💡 This means the bridge is working!")
            print("❓ But no Colab processor is running to process them")
            return "queued"
        
        else:
            print(f"❌ Error: {result1.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    result = test_basic_colab()
    
    if result == True:
        print("\n🎉 COLAB IS WORKING!")
        print("✅ Code execution successful")
        print("✅ Python environment active")
        print("✅ Ready for hybrid testing")
    elif result == "queued":
        print("\n⏳ COLAB BRIDGE WORKING")
        print("✅ Commands are being sent")
        print("❓ Need active processor to execute them")
        print("🔧 This explains why your cells run in 0ms")
    else:
        print("\n❌ COLAB NOT RESPONDING")
        print("🔧 Need to debug connection issues")