#!/usr/bin/env python3
"""
Quick test of the hybrid experience
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def quick_hybrid_test():
    """Quick test of hybrid functionality"""
    print("⚡ Quick Hybrid Test")
    print("=" * 30)
    
    try:
        bridge = UniversalColabBridge("quick_test")
        bridge.initialize()
        
        print("✅ Connected to Google Drive")
        
        # Send simple test
        print("📤 Sending test to Colab...")
        result = bridge.execute_code("""
print("🎉 HYBRID SUCCESS!")
print("✅ Code written locally")
print("✅ Executed on Google Colab") 
print("✅ Results back to local")

import datetime
print(f"⏰ Executed at: {datetime.datetime.now()}")

# Test GPU if available
try:
    import torch
    if torch.cuda.is_available():
        print(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("💻 CPU mode")
except:
    print("💻 CPU mode")

print("🎯 Your 'basically local google colab notebook' is WORKING!")
""", timeout=20)
        
        if result.get('status') == 'success':
            print("🎉 SUCCESS! HYBRID EXPERIENCE WORKING!")
            print("=" * 50)
            print("📤 Output from Colab:")
            print(result.get('output', ''))
            print("=" * 50)
            print("✅ Your vision achieved:")
            print("  • Local code writing")
            print("  • Colab cloud execution") 
            print("  • Direct local results")
            print("  • 'Basically local google colab notebook' ✅")
            return True
        
        elif result.get('status') == 'queued':
            print("⏳ Request queued - processor may be starting up")
            print("Wait a moment and try again")
            return False
        
        else:
            print(f"❌ Error: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = quick_hybrid_test()
    
    if success:
        print("\n🚀 READY FOR FULL TESTING!")
        print("Your hybrid experience is working perfectly!")
    else:
        print("\n⏳ Try again in a moment...")
        print("The processor may still be starting up")