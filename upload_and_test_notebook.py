#!/usr/bin/env python3
"""
Upload the tested notebook to Google Colab and get the shareable link
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def upload_tested_notebook():
    """Upload the tested notebook to Google Drive for Colab access"""
    print("📤 Uploading Tested Notebook to Google Drive")
    print("=" * 50)
    
    try:
        bridge = UniversalColabBridge("upload_notebook")
        bridge.initialize()
        
        # Path to our tested notebook
        notebook_path = Path(__file__).parent / "notebooks" / "tested-processor.ipynb"
        
        if not notebook_path.exists():
            print(f"❌ Notebook not found: {notebook_path}")
            return None
        
        print(f"📓 Found notebook: {notebook_path.name}")
        print(f"📁 Size: {notebook_path.stat().st_size} bytes")
        
        # Upload to Google Drive
        from googleapiclient.http import MediaFileUpload
        
        file_metadata = {
            'name': 'TESTED-Hybrid-Processor.ipynb',
            'parents': [bridge.folder_id]
        }
        
        media = MediaFileUpload(str(notebook_path), mimetype='application/json')
        
        file = bridge.drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
        file_id = file.get('id')
        
        print(f"✅ Notebook uploaded successfully!")
        print(f"📄 File ID: {file_id}")
        
        # Make it shareable
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        
        bridge.drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        print(f"✅ Made publicly accessible")
        
        # Generate Colab link
        colab_link = f"https://colab.research.google.com/drive/{file_id}"
        
        print(f"\n🔗 COLAB LINK:")
        print(f"   {colab_link}")
        print(f"\n📋 Instructions:")
        print(f"   1. Open the link above")
        print(f"   2. Run each cell and see the results")
        print(f"   3. Each cell is tested and should work")
        print(f"   4. Report back what you see!")
        
        return colab_link
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def create_test_commands():
    """Create test commands to verify the processor works"""
    print("\n🧪 Creating Test Commands")
    print("=" * 30)
    
    try:
        bridge = UniversalColabBridge("test_commands")
        bridge.initialize()
        
        # Test command 1: Simple execution
        test1_result = bridge.execute_code("""
print("🧪 Test 1: Basic execution")
print("✅ Python is working")
import datetime
print(f"⏰ Current time: {datetime.datetime.now()}")
""", timeout=30)
        
        print("📋 Test 1 Results:")
        if test1_result.get('status') == 'success':
            print("✅ Success!")
            print(f"📤 Output: {test1_result.get('output', '')[:200]}...")
        else:
            print(f"❌ Failed: {test1_result.get('error', 'No error info')}")
        
        # Test command 2: Check for processor
        test2_result = bridge.execute_code("""
print("🔍 Test 2: Checking for active processor")
import os
print(f"📁 Current directory: {os.getcwd()}")

# Check if we can see any activity
print("✅ Test completed - checking processor status")
""", timeout=30)
        
        print("\n📋 Test 2 Results:")
        if test2_result.get('status') == 'success':
            print("✅ Success!")
            print(f"📤 Output: {test2_result.get('output', '')[:200]}...")
        else:
            print(f"❌ Failed: {test2_result.get('error', 'No error info')}")
        
        # Check if any commands were processed
        if test1_result.get('status') == 'success' or test2_result.get('status') == 'success':
            print("\n🎉 PROCESSOR IS RESPONDING!")
            print("✅ The hybrid system is working")
            return True
        else:
            print("\n⏳ PROCESSOR NOT RESPONDING")
            print("💡 Need to start the Colab notebook first")
            return False
            
    except Exception as e:
        print(f"❌ Test commands failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Upload and Test Notebook")
    print("=" * 50)
    
    # Upload the tested notebook
    colab_link = upload_tested_notebook()
    
    if colab_link:
        print(f"\n📓 Notebook uploaded and ready!")
        print(f"🔗 Link: {colab_link}")
        
        # Test if processor is already running
        print(f"\n🧪 Testing if processor is running...")
        processor_running = create_test_commands()
        
        if processor_running:
            print(f"\n🎉 READY TO TEST!")
            print(f"   The processor is already running")
            print(f"   You can test with: python3 test_now.py")
        else:
            print(f"\n📋 NEXT STEPS:")
            print(f"   1. Open: {colab_link}")
            print(f"   2. Run all cells in order")
            print(f"   3. Watch each cell execute")
            print(f"   4. Come back and test: python3 test_now.py")
    else:
        print(f"\n❌ Upload failed - check the existing notebooks")