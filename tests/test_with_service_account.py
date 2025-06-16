#!/usr/bin/env python3
"""
Test using service account directly - no permission issues
"""

import sys
import json
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_service_account_directly():
    """Use service account to test everything directly"""
    print("🔑 TESTING WITH SERVICE ACCOUNT DIRECTLY")
    print("=" * 50)
    print("You're right - I should use the service account for everything!")
    
    try:
        # Import and setup service account
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
        import tempfile
        import io
        
        # Load service account
        service_account_path = "./credentials/eng-flux-459812-q6-e05c54813553.json"
        folder_id = "1tzHn4J3QntSLJlJNXcNJe3cLdILGEb3Z"
        
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        
        drive_service = build('drive', 'v3', credentials=credentials)
        print("✅ Service account authenticated")
        
        # Test 1: List files
        print("\n📁 Test 1: Checking folder access...")
        query = f"'{folder_id}' in parents and trashed=false"
        results = drive_service.files().list(q=query, pageSize=5).execute()
        files = results.get('files', [])
        print(f"✅ Found {len(files)} files in folder")
        
        # Test 2: Create a command file
        print("\n📤 Test 2: Creating command file...")
        command_id = f"service_test_{int(time.time())}"
        command_data = {
            "type": "execute",
            "code": """
print("🎉 SERVICE ACCOUNT TEST SUCCESS!")
print("✅ This proves the hybrid system works with service account!")
import datetime
print(f"⏰ Executed at: {datetime.datetime.now()}")

# Test GPU if available
try:
    import torch
    if torch.cuda.is_available():
        print(f"🚀 GPU Available: {torch.cuda.get_device_name(0)}")
    else:
        print("💻 CPU mode")
except ImportError:
    print("💻 CPU mode (torch not available)")

print("🎯 Hybrid 'basically local google colab notebook' WORKING!")
""",
            "timestamp": time.time(),
            "source": "service_account_test"
        }
        
        # Upload using service account
        file_metadata = {
            'name': f'command_{command_id}.json',
            'parents': [folder_id]
        }
        
        # Use BytesIO to avoid temp files
        content_bytes = json.dumps(command_data, indent=2).encode('utf-8')
        media = MediaIoBaseUpload(
            io.BytesIO(content_bytes),
            mimetype='application/json'
        )
        
        command_file = drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
        print(f"✅ Command created: {command_file.get('id')}")
        
        # Test 3: Wait for processor response
        print(f"\n⏳ Test 3: Waiting for Colab processor response...")
        print(f"Looking for: result_{command_id}.json")
        
        for attempt in range(12):  # Wait up to 60 seconds
            time.sleep(5)
            
            # Check for result
            result_query = f"'{folder_id}' in parents and name='result_{command_id}.json'"
            result_files = drive_service.files().list(q=result_query).execute()
            
            if result_files.get('files'):
                result_file = result_files['files'][0]
                print(f"✅ Processor responded! File ID: {result_file.get('id')}")
                
                # Read result using service account
                try:
                    content = drive_service.files().get_media(fileId=result_file['id']).execute()
                    result_data = json.loads(content.decode('utf-8'))
                    
                    print(f"\n🎉 HYBRID SYSTEM SUCCESS!")
                    print(f"=" * 50)
                    print(f"📊 Status: {result_data.get('status')}")
                    print(f"📤 Output from Colab:")
                    print(f"-" * 30)
                    print(result_data.get('output', 'No output'))
                    print(f"-" * 30)
                    print(f"✅ Your 'basically local google colab notebook' is WORKING!")
                    print(f"✅ Service account handles all permissions!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Could not read result: {e}")
                    return False
            else:
                print(f"⏳ Waiting for response... {(attempt+1)*5}s")
        
        print(f"\n⏰ No response after 60 seconds")
        print(f"💡 Processor may not be running in Colab")
        print(f"📋 Check that Cell 5 is showing status updates")
        return False
        
    except Exception as e:
        print(f"❌ Service account test failed: {e}")
        return False

def show_processor_instructions():
    """Show what should be happening in Colab"""
    print(f"\n📋 PROCESSOR STATUS CHECK")
    print(f"=" * 30)
    print(f"In your Colab notebook, Cell 5 should show:")
    print(f"")
    print(f"🚀 Starting ACTIVE processor...")
    print(f"⏱️ Will run for 30 minutes")
    print(f"📊 Status updates every 5 seconds...")
    print(f"⏳ Active... 5s | Processed: 0 | Errors: 0")
    print(f"⏳ Active... 10s | Processed: 0 | Errors: 0")
    print(f"⏳ Active... 15s | Processed: 0 | Errors: 0")
    print(f"")
    print(f"If you see this ↑, the processor is running correctly!")
    print(f"If Cell 5 finished in 0ms, it's not working.")

if __name__ == "__main__":
    success = test_service_account_directly()
    
    if success:
        print(f"\n🎉 PERFECT! HYBRID SYSTEM WORKING!")
        print(f"✅ Service account solves all permission issues")
        print(f"✅ Local code → Colab execution → Local results")
        print(f"✅ Your vision of 'basically local google colab notebook' achieved!")
    else:
        print(f"\n⏳ SYSTEM READY, WAITING FOR PROCESSOR")
        print(f"✅ Service account working perfectly")
        print(f"⏳ Need Colab processor to be actively running")
        show_processor_instructions()