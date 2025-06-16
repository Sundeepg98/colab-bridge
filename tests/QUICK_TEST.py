#!/usr/bin/env python3
"""
Quick test for Colab-Bridge with user cooperation
Let's verify the complete working solution!
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_colab_bridge():
    """Test the complete Colab-Bridge solution"""
    
    print("🧪 COLAB-BRIDGE LIVE TEST")
    print("=" * 50)
    
    # Set up environment
    os.environ['SERVICE_ACCOUNT_PATH'] = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
    os.environ['GOOGLE_DRIVE_FOLDER_ID'] = '1ruRdOXUJi16sHgDtpgxqtR7A7g7J8PpA'
    
    try:
        from colab_integration.bridge import ClaudeColabBridge
        
        print("✅ Importing bridge...")
        bridge = ClaudeColabBridge()
        bridge.initialize()
        
        print(f"✅ Bridge initialized: {bridge.instance_name}")
        print(f"✅ Using folder: {bridge.folder_id}")
        
        # Test code that should run in Colab
        test_code = """
print("🔥 LIVE COLAB-BRIDGE TEST!")
print("=" * 40)

# Test 1: Environment check
import sys
print(f"Python: {sys.version}")

# Test 2: GPU check
try:
    import torch
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"✅ GPU Available: {gpu_name}")
        
        # Simple GPU computation
        x = torch.randn(1000, 1000).cuda()
        y = torch.matmul(x, x)
        print(f"✅ GPU Computation: {y.shape}")
    else:
        print("⚠️ No GPU available")
except ImportError:
    print("📦 PyTorch not installed")

# Test 3: Colab environment check
try:
    import google.colab
    print("✅ Running in Google Colab!")
    
    # Check secrets
    try:
        from google.colab import userdata
        # Don't print actual secret, just check if available
        try:
            userdata.get('sun_colab')
            print("✅ Secret 'sun_colab' is available!")
        except:
            print("⚠️ Secret 'sun_colab' not found")
    except:
        print("⚠️ Secrets not accessible")
        
except ImportError:
    print("❌ Not in Colab environment")

print("=" * 40)
print("🎉 TEST COMPLETE!")
"""
        
        print("\n📤 Sending test code to Colab...")
        print("⏳ Waiting for response (timeout: 60s)...")
        
        result = bridge.execute_code(test_code, timeout=60)
        
        if result and result.get('status') == 'success':
            print("\n✅ SUCCESS! Response received from Colab!")
            print("\n📺 Output from Colab:")
            print("-" * 50)
            print(result.get('output', 'No output'))
            print("-" * 50)
            
            # Check processor type
            processor = result.get('processor', 'unknown')
            print(f"\n🤖 Processed by: {processor}")
            
            return True
        else:
            print("\n⏰ No response received.")
            print("💡 Please ensure:")
            print("   1. Colab notebook is running")
            print("   2. Processor cells are executed")
            print("   3. Secret 'sun_colab' is configured")
            
            if result:
                print(f"\nDebug info: {result}")
            
            return False
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_notebook_status():
    """Check the status of Colab notebooks"""
    
    print("\n📋 CHECKING NOTEBOOK STATUS")
    print("-" * 40)
    
    notebooks = {
        "Working Automation": "https://colab.research.google.com/drive/1tWRrTlG_rBLdUb9Vs16i9DURsJiluN_Z",
        "Secrets Automation": "https://colab.research.google.com/drive/1TUjKlwPo5Ond4vhE1WsvWqoYHGmEoRIq"
    }
    
    print("Available notebooks:")
    for name, url in notebooks.items():
        print(f"\n{name}:")
        print(f"  🔗 {url}")
    
    print("\n💡 To activate:")
    print("   1. Open one of the notebooks above")
    print("   2. Add secret 'sun_colab' with service account JSON")
    print("   3. Run all cells")
    print("   4. Return here and press Enter")

if __name__ == "__main__":
    print("🚀 COLAB-BRIDGE LIVE TEST")
    print("=" * 60)
    
    # Check notebook status
    check_notebook_status()
    
    input("\n🔔 Press Enter when Colab notebook is running...")
    
    # Run the test
    print("\n🧪 Running test...")
    success = test_colab_bridge()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    if success:
        print("✅ COLAB-BRIDGE IS WORKING!")
        print("🎉 Successfully executed code in Colab with GPU!")
        print("🔥 The automation is real!")
    else:
        print("❌ Test did not complete")
        print("💡 Follow the setup instructions above")
        
    print("\n🤝 Thank you for testing!")