#!/usr/bin/env python3
"""
Simulate the Colab processor locally to show complete test results
"""

import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

from colab_integration.bridge import ClaudeColabBridge
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

class LocalColabSimulator:
    """Simulate what the Colab processor does"""
    
    def __init__(self, service_account_path, folder_id):
        self.folder_id = folder_id
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        self.drive_service = build('drive', 'v3', credentials=credentials)
    
    def get_pending_requests(self):
        """Get unprocessed requests"""
        query = f"'{self.folder_id}' in parents and name contains 'command_' and trashed=false"
        results = self.drive_service.files().list(
            q=query,
            fields="files(id, name, createdTime)",
            orderBy="createdTime"
        ).execute()
        return results.get('files', [])
    
    def read_request(self, file_id):
        """Read request content"""
        content = self.drive_service.files().get_media(fileId=file_id).execute()
        return json.loads(content.decode('utf-8'))
    
    def execute_code(self, code):
        """Execute code like Colab would"""
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Create clean namespace
            namespace = {'__name__': '__main__'}
            exec(code, namespace)
            output = sys.stdout.getvalue()
            
            return {
                'status': 'success',
                'output': output,
                'timestamp': time.time()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
        finally:
            sys.stdout = old_stdout
    
    def write_response(self, command_id, response_data):
        """Write response back to Drive"""
        response_name = f'result_{command_id}.json'
        
        file_metadata = {
            'name': response_name,
            'parents': [self.folder_id]
        }
        
        media = MediaIoBaseUpload(
            io.BytesIO(json.dumps(response_data, indent=2).encode('utf-8')),
            mimetype='application/json'
        )
        
        file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name'
        ).execute()
        
        return file
    
    def process_one_request(self):
        """Process one pending request"""
        requests = self.get_pending_requests()
        if not requests:
            return None
        
        # Take the oldest request
        request_file = requests[0]
        print(f"📋 Processing: {request_file['name']}")
        
        # Read request
        request_data = self.read_request(request_file['id'])
        command_id = request_file['name'].replace('command_', '').replace('.json', '')
        
        print(f"📄 Code to execute:")
        print("-" * 40)
        print(request_data.get('code', 'No code'))
        print("-" * 40)
        
        # Execute
        print("⚡ Executing...")
        result = self.execute_code(request_data.get('code', ''))
        
        # Write response
        response_file = self.write_response(command_id, result)
        
        print(f"✅ Response written: {response_file['name']}")
        
        # Delete processed request to avoid reprocessing
        self.drive_service.files().delete(fileId=request_file['id']).execute()
        print(f"🗑️  Cleaned up request: {request_file['name']}")
        
        return result

def main():
    print("🎭 Simulating Colab Processor Locally")
    print("=" * 50)
    
    # Create a simple test request first
    print("📤 Creating minimal test request...")
    
    bridge = ClaudeColabBridge()
    bridge.initialize()
    
    # Minimal test code
    test_code = '''
print("✅ Minimal test successful!")
print(f"Time: {time.time()}")

import sys
print(f"Python: {sys.version}")

# Simple computation
result = 2 + 2
print(f"2 + 2 = {result}")
'''
    
    # Send test request
    result = bridge.execute_code(test_code, timeout=1)  # Quick timeout since we'll process locally
    
    if 'request_id' in result:
        print(f"✅ Test request created: {result['request_id']}")
    else:
        print("⏳ Request queued for processing")
    
    print("\n🎭 Now simulating Colab processor...")
    
    # Simulate processor
    simulator = LocalColabSimulator(
        service_account_path=os.getenv('SERVICE_ACCOUNT_PATH'),
        folder_id=os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    )
    
    # Process the request
    result = simulator.process_one_request()
    
    if result:
        print("\n📋 EXECUTION RESULT:")
        print("=" * 50)
        print(f"Status: {result['status']}")
        
        if result['status'] == 'success':
            print("\n📤 Output from simulated Colab:")
            print(result['output'])
        else:
            print(f"\n❌ Error: {result['error']}")
        
        print("=" * 50)
        print("✅ Complete request-response cycle demonstrated!")
    else:
        print("❌ No requests to process")

if __name__ == "__main__":
    main()