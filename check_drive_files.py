#!/usr/bin/env python3
"""
Check what's happening with Drive files
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.universal_bridge import UniversalColabBridge

def check_drive_status():
    """Check Drive folder and files"""
    print("🔍 CHECKING DRIVE STATUS")
    print("=" * 30)
    
    try:
        bridge = UniversalColabBridge("drive_check")
        bridge.initialize()
        
        # List files in the folder
        print("📁 Checking folder contents...")
        query = f"'{bridge.folder_id}' in parents and trashed=false"
        results = bridge.drive_service.files().list(
            q=query, 
            fields="files(id, name, createdTime, owners)",
            orderBy="createdTime desc",
            maxResults=10
        ).execute()
        
        files = results.get('files', [])
        print(f"📊 Found {len(files)} files in folder")
        
        command_files = []
        result_files = []
        
        for file in files:
            print(f"📄 {file['name']} (ID: {file['id'][:20]}...)")
            if file['name'].startswith('command_'):
                command_files.append(file)
            elif file['name'].startswith('result_'):
                result_files.append(file)
        
        print(f"\n📊 Summary:")
        print(f"   📤 Command files: {len(command_files)}")
        print(f"   📥 Result files: {len(result_files)}")
        
        if command_files:
            print(f"\n📤 Recent commands:")
            for cmd in command_files[:3]:
                print(f"   - {cmd['name']}")
        
        if result_files:
            print(f"\n📥 Recent results:")
            for res in result_files[:3]:
                print(f"   - {res['name']}")
        
        # Check if processor is creating files
        if len(command_files) > len(result_files):
            print(f"\n⏳ Processor status: Commands waiting for processing")
            print(f"   {len(command_files) - len(result_files)} commands pending")
        elif len(result_files) > 0:
            print(f"\n✅ Processor status: Active (results being generated)")
        else:
            print(f"\n❓ Processor status: No activity detected")
        
        return len(files) > 0
        
    except Exception as e:
        print(f"❌ Drive check failed: {e}")
        return False

def simple_processor_test():
    """Try to create a simple command"""
    print("\n🧪 SIMPLE PROCESSOR TEST")
    print("=" * 30)
    
    try:
        bridge = UniversalColabBridge("simple_test")
        bridge.initialize()
        
        # Create a simple command manually
        import json
        import time
        import tempfile
        from googleapiclient.http import MediaFileUpload
        
        command_id = f"test_{int(time.time())}"
        command_data = {
            "type": "execute",
            "code": "print('Hello from processor test!')",
            "timestamp": time.time(),
            "source": "manual_test"
        }
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(command_data, f, indent=2)
            temp_path = f.name
        
        # Upload command
        file_metadata = {
            'name': f'command_{command_id}.json',
            'parents': [bridge.folder_id]
        }
        
        media = MediaFileUpload(temp_path, mimetype='application/json')
        
        file = bridge.drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
        import os
        os.unlink(temp_path)
        
        print(f"✅ Created test command: command_{command_id}.json")
        print(f"📄 File ID: {file.get('id')}")
        
        # Wait for result
        print("⏳ Waiting for processor to respond...")
        for i in range(6):  # Wait up to 30 seconds
            time.sleep(5)
            
            # Check for result file
            result_query = f"'{bridge.folder_id}' in parents and name='result_{command_id}.json'"
            result_files = bridge.drive_service.files().list(q=result_query).execute()
            
            if result_files.get('files'):
                print(f"✅ Processor responded! Found result file.")
                
                # Try to read result
                result_file = result_files['files'][0]
                try:
                    content = bridge.drive_service.files().get_media(fileId=result_file['id']).execute()
                    result_data = json.loads(content.decode('utf-8'))
                    
                    print(f"📊 Result status: {result_data.get('status')}")
                    if result_data.get('output'):
                        print(f"📤 Output: {result_data.get('output')}")
                    
                    return True
                except Exception as e:
                    print(f"❌ Could not read result: {e}")
                    return False
            else:
                print(f"⏳ Waiting... {(i+1)*5}s")
        
        print("⏰ Timeout - processor may not be running")
        return False
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 DIAGNOSING HYBRID SYSTEM")
    print("=" * 40)
    
    # Check drive
    drive_ok = check_drive_status()
    
    if drive_ok:
        # Test processor
        processor_ok = simple_processor_test()
        
        if processor_ok:
            print("\n🎉 HYBRID SYSTEM WORKING!")
            print("✅ Drive access: OK")
            print("✅ Processor: Responding")
            print("✅ Ready for hybrid development!")
        else:
            print("\n⏳ PROCESSOR NOT RESPONDING")
            print("✅ Drive access: OK") 
            print("❌ Processor: Not running or slow")
            print("💡 Check Cell 5 in Colab is showing status updates")
    else:
        print("\n❌ DRIVE ACCESS ISSUES")
        print("🔧 Check credentials and permissions")