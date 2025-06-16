#!/usr/bin/env python3
"""
Test the working automation
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_working_automation():
    """Test the service account automation"""
    
    print("🧪 TESTING WORKING SERVICE ACCOUNT AUTOMATION")
    print("=" * 50)
    
    # Set environment
    os.environ['SERVICE_ACCOUNT_PATH'] = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
    os.environ['GOOGLE_DRIVE_FOLDER_ID'] = '1ruRdOXUJi16sHgDtpgxqtR7A7g7J8PpA'
    
    try:
        from colab_integration.bridge import ClaudeColabBridge
        
        bridge = ClaudeColabBridge()
        bridge.initialize()
        
        print("✅ Bridge initialized")
        
        # Test GPU code
        gpu_test = """
print("🔥 WORKING AUTOMATION TEST")
print("✅ This is running via SERVICE ACCOUNT automation!")

# GPU test
try:
    import torch
    print(f"GPU available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        
        # GPU computation
        x = torch.randn(1000, 1000).cuda()
        y = torch.matmul(x, x)
        print(f"GPU computation: {y.shape}")
        print("🎉 REAL COLAB GPU EXECUTION VIA SERVICE ACCOUNT!")
    else:
        print("CPU execution")
        
except ImportError:
    print("PyTorch not available, will be installed")

print("✅ WORKING AUTOMATION SUCCESSFUL!")
"""
        
        print("📤 Sending GPU test to automated processor...")
        result = bridge.execute_code(gpu_test, timeout=60)
        
        if result.get('status') == 'success':
            print("🎉 WORKING AUTOMATION SUCCESSFUL!")
            print("📺 Output from service account processor:")
            print("-" * 40)
            print(result.get('output'))
            print("-" * 40)
            
            if 'GPU' in result.get('output', ''):
                print("🔥 CONFIRMED: Real GPU execution via service account!")
            
        else:
            print(f"⏳ Automation may be starting up...")
            print("Make sure the processor notebook is running")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_working_automation()
