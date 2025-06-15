#!/usr/bin/env python3
"""
Claude Tools Basic Test
Simple test to verify the setup works
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from colab_integration.bridge import ClaudeColabBridge

def test_basic_setup():
    """Test basic setup and configuration"""
    print("🧪 Claude Tools Basic Test")
    print("==========================")
    
    # Test 1: Environment variables
    print("\n1. Testing environment configuration...")
    
    required_env = ['SERVICE_ACCOUNT_PATH', 'GOOGLE_DRIVE_FOLDER_ID']
    missing_env = []
    
    for env_var in required_env:
        if not os.getenv(env_var):
            missing_env.append(env_var)
    
    if missing_env:
        print(f"❌ Missing environment variables: {', '.join(missing_env)}")
        print("Please check your .env file")
        return False
    
    print("✅ Environment variables configured")
    
    # Test 2: Bridge initialization
    print("\n2. Testing bridge initialization...")
    
    try:
        bridge = ClaudeColabBridge()
        print("✅ Bridge created successfully")
    except Exception as e:
        print(f"❌ Bridge creation failed: {e}")
        return False
    
    # Test 3: Google Drive connection
    print("\n3. Testing Google Drive connection...")
    
    try:
        bridge.initialize()
        print("✅ Google Drive connection successful")
    except Exception as e:
        print(f"❌ Google Drive connection failed: {e}")
        print("Please check your service account configuration")
        return False
    
    print("\n🎉 All basic tests passed!")
    print("Claude Tools is ready to use")
    return True

def test_simple_execution():
    """Test simple code execution (requires active Colab)"""
    print("\n4. Testing code execution (requires active Colab processor)...")
    
    try:
        bridge = ClaudeColabBridge()
        bridge.initialize()
        
        # Simple test code
        test_code = "print('Hello from Claude Tools!')"
        result = bridge.execute_code(test_code, timeout=10)
        
        if result.get('success'):
            print("✅ Code execution successful")
            print(f"Output: {result.get('output', 'No output')}")
            return True
        else:
            print(f"⚠️ Code execution failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"⚠️ Code execution test failed: {e}")
        print("This is normal if no Colab processor is running")
        return False

if __name__ == "__main__":
    success = test_basic_setup()
    
    if success:
        # Only test execution if basic setup works
        test_simple_execution()
    
    if not success:
        sys.exit(1)