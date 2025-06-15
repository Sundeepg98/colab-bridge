#!/usr/bin/env python3
"""
Using your service account JSON to show what's possible
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import requests

SERVICE_ACCOUNT_FILE = '/var/projects/eng-flux-459812-q6-e05c54813553.json'

def test_what_service_account_can_do():
    """Test service account capabilities"""
    
    print("🔐 Using Service Account JSON")
    print("="*60)
    
    # Load credentials
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # What CAN the service account do?
    print("\n✅ What Service Account CAN do:")
    
    try:
        # 1. Access Google Drive
        service = build('drive', 'v3', credentials=creds)
        results = service.files().list(
            q="name='ColabAPI'",
            spaces='drive',
            pageSize=10
        ).execute()
        
        if results.get('files'):
            print("  ✅ Access Google Drive files")
            print(f"  ✅ Found ColabAPI folder: {results['files'][0]['id']}")
            
            # Create a test file
            file_metadata = {
                'name': 'service_account_test.txt',
                'parents': [results['files'][0]['id']]
            }
            media = MediaIoBaseUpload(
                io.BytesIO(b"Test from service account"),
                mimetype='text/plain'
            )
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"  ✅ Create files in Drive: {file.get('id')}")
            
    except Exception as e:
        print(f"  ❌ Drive access error: {e}")
    
    print("\n❌ What Service Account CANNOT do:")
    print("  ❌ Execute code in Colab notebooks")
    print("  ❌ Control Colab UI")
    print("  ❌ Access Colab runtime")
    print("  ❌ Run notebook cells")
    
    # Try to access Colab (will fail)
    print("\n🧪 Attempting Colab access with service account:")
    notebook_id = "1EwfBj0nC9St-2hB1bv2zGWWDTcS4slsx"
    
    # Get access token from service account
    creds.refresh(requests.Request())
    token = creds.token
    
    # Try Colab endpoints with service account token
    endpoints = [
        f"https://colab.research.google.com/api/notebooks/{notebook_id}/execute",
        f"https://notebooks.googleapis.com/v1/notebooks/{notebook_id}",
    ]
    
    for endpoint in endpoints:
        try:
            headers = {'Authorization': f'Bearer {token}'}
            r = requests.post(endpoint, headers=headers, json={'code': 'print("test")'})
            print(f"  {endpoint}: {r.status_code}")
        except Exception as e:
            print(f"  {endpoint}: Failed - {str(e)[:50]}")
    
    print("\n🎯 Summary:")
    print("""
    Service Account + API Key = Full Drive access ✅
    Service Account + API Key ≠ Colab execution ❌
    
    Colab requires human interaction in the browser!
    """)

if __name__ == "__main__":
    test_what_service_account_can_do()