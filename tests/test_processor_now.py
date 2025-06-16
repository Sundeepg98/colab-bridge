#!/usr/bin/env python3
"""
Test if the processor is actually running by checking for responses
"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def test_processor_activity():
    """Test if processor is responding"""
    print("🧪 TESTING PROCESSOR ACTIVITY")
    print("=" * 40)
    
    try:
        bridge = UniversalColabBridge("processor_test")
        bridge.initialize()
        
        # Send a simple test
        print("📤 Sending simple test command...")
        result = bridge.execute_code("""
print("🎉 SUCCESS! Processor is working!")
print("✅ Your hybrid experience is active!")
import datetime
print(f"⏰ Time: {datetime.datetime.now()}")
""", timeout=25)
        
        print(f"\n📊 Result Status: {result.get('status')}")
        
        if result.get('status') == 'success':
            print("🎉 HYBRID PROCESSOR WORKING!")
            print("=" * 50)
            print("📤 Output from Colab:")
            print(result.get('output', ''))
            print("=" * 50)
            print("✅ Your 'basically local google colab notebook' is ACTIVE!")
            return True
            
        elif result.get('status') == 'queued':
            print("⏳ Command was queued")
            print("💡 Processor might be starting up...")
            
            # Wait a moment and try again
            print("⏳ Waiting 10 seconds and trying again...")
            time.sleep(10)
            
            # Try once more
            result2 = bridge.execute_code("print('Second test')", timeout=15)
            if result2.get('status') == 'success':
                print("🎉 PROCESSOR RESPONDED ON SECOND TRY!")
                print(f"📤 Output: {result2.get('output')}")
                return True
            else:
                print("⏳ Still queued - processor may need more time")
                return "queued"
        
        else:
            print(f"❌ Error: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    result = test_processor_activity()
    
    if result == True:
        print("\n🚀 READY TO USE!")
        print("Your hybrid system is working perfectly!")
        print("You can now write code locally and execute on Colab!")
    elif result == "queued":
        print("\n⏳ PROCESSOR STARTING UP")
        print("Wait a minute for Cell 5 to fully initialize")
    else:
        print("\n❌ PROCESSOR NOT RESPONDING")
        print("Check that Cell 5 is running and showing status updates")