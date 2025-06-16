#!/usr/bin/env python3
"""
Test if we can execute Colab cells using service account via API
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

def test_colab_execution_api():
    """Test various approaches to execute Colab cells with service account"""
    
    print("🔬 TESTING COLAB CELL EXECUTION VIA API")
    print("=" * 50)
    
    try:
        import google.auth.transport.requests
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # Load service account
        creds_path = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
        
        with open(creds_path) as f:
            sa_info = json.load(f)
        
        # Try different scopes for Colab access
        scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/colab',
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/compute',
            'https://www.googleapis.com/auth/notebooks'
        ]
        
        credentials = service_account.Credentials.from_service_account_info(
            sa_info, scopes=scopes
        )
        
        print("✅ Service account loaded with extended scopes")
        
        # Test different API approaches
        test_colab_api_direct(credentials)
        test_notebooks_api(credentials)
        test_compute_api(credentials)
        test_drive_execution(credentials)
        
    except Exception as e:
        print(f"❌ Setup error: {e}")

def test_colab_api_direct(credentials):
    """Test direct Colab API calls"""
    
    print("\n🧪 Testing Direct Colab API")
    print("-" * 35)
    
    try:
        import google.auth.transport.requests
        
        # Refresh credentials
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        
        headers = {
            'Authorization': f'Bearer {credentials.token}',
            'Content-Type': 'application/json'
        }
        
        # Try different Colab API endpoints
        endpoints_to_test = [
            'https://colab.research.google.com/api/kernels',
            'https://colab.research.google.com/api/sessions',
            'https://colab.research.google.com/api/contents',
            'https://colaboratory.jupyter.org/api/kernels',
            'https://colab.research.google.com/api/v1/kernels'
        ]
        
        for endpoint in endpoints_to_test:
            try:
                print(f"🔍 Testing: {endpoint}")
                response = requests.get(endpoint, headers=headers, timeout=10)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ SUCCESS! Found working endpoint")
                    print(f"   Response: {response.json()}")
                    return True
                elif response.status_code == 401:
                    print(f"   ❌ Unauthorized - need different auth")
                elif response.status_code == 404:
                    print(f"   ❌ Not found")
                else:
                    print(f"   ⚠️ Status {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("❌ No working Colab API endpoints found")
        return False
        
    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        return False

def test_notebooks_api(credentials):
    """Test Google Cloud Notebooks API"""
    
    print("\n🧪 Testing Cloud Notebooks API")
    print("-" * 35)
    
    try:
        notebooks_service = build('notebooks', 'v1', credentials=credentials)
        print("✅ Notebooks API service created")
        
        # List instances
        project_id = 'automation-engine-463103'
        location = 'us-central1-a'
        
        request = notebooks_service.projects().locations().instances().list(
            parent=f'projects/{project_id}/locations/{location}'
        )
        
        response = request.execute()
        print(f"✅ Notebooks API working: {response}")
        
        # Try to create a notebook instance
        return test_create_notebook_instance(notebooks_service, project_id, location)
        
    except Exception as e:
        print(f"❌ Notebooks API test failed: {e}")
        return False

def test_create_notebook_instance(notebooks_service, project_id, location):
    """Try to create a notebook instance"""
    
    print("🚀 Attempting to create notebook instance...")
    
    try:
        instance_body = {
            'machineType': f'projects/{project_id}/zones/{location}/machineTypes/n1-standard-1',
            'vmImage': {
                'project': 'deeplearning-platform-release',
                'imageFamily': 'tf-latest-gpu'
            }
        }
        
        request = notebooks_service.projects().locations().instances().create(
            parent=f'projects/{project_id}/locations/{location}',
            instanceId='automated-colab-instance',
            body=instance_body
        )
        
        response = request.execute()
        print(f"✅ Notebook instance creation started: {response}")
        return True
        
    except Exception as e:
        print(f"❌ Instance creation failed: {e}")
        return False

def test_compute_api(credentials):
    """Test Compute Engine API for VM creation"""
    
    print("\n🧪 Testing Compute Engine API")
    print("-" * 35)
    
    try:
        compute_service = build('compute', 'v1', credentials=credentials)
        print("✅ Compute API service created")
        
        project_id = 'automation-engine-463103'
        
        # List zones
        zones_request = compute_service.zones().list(project=project_id)
        zones_response = zones_request.execute()
        
        print(f"✅ Can access Compute API: {len(zones_response.get('items', []))} zones")
        
        # Try to create a VM with Jupyter
        return test_create_jupyter_vm(compute_service, project_id)
        
    except Exception as e:
        print(f"❌ Compute API test failed: {e}")
        return False

def test_create_jupyter_vm(compute_service, project_id):
    """Try to create a VM with Jupyter"""
    
    print("🚀 Attempting to create Jupyter VM...")
    
    try:
        zone = 'us-central1-a'
        
        # VM configuration
        config = {
            'name': 'automated-jupyter-vm',
            'machineType': f'projects/{project_id}/zones/{zone}/machineTypes/n1-standard-1',
            'disks': [{
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/deeplearning-platform-release/global/images/family/tf-latest-gpu'
                }
            }],
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}]
            }],
            'metadata': {
                'items': [{
                    'key': 'startup-script',
                    'value': '''#!/bin/bash
echo "Starting Jupyter automation..."
jupyter lab --ip=0.0.0.0 --port=8080 --no-browser --allow-root
'''
                }]
            }
        }
        
        request = compute_service.instances().insert(
            project=project_id,
            zone=zone,
            body=config
        )
        
        response = request.execute()
        print(f"✅ VM creation started: {response}")
        return True
        
    except Exception as e:
        print(f"❌ VM creation failed: {e}")
        return False

def test_drive_execution(credentials):
    """Test executing code by manipulating Drive files"""
    
    print("\n🧪 Testing Drive-Based Execution")
    print("-" * 35)
    
    try:
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # Create a Python script
        script_content = '''
#!/usr/bin/env python3
"""
Automated execution script
"""

import os
import json
import time
from datetime import datetime

print("🚀 AUTOMATED EXECUTION VIA DRIVE")
print(f"Time: {datetime.now()}")

# Check if we're in Colab
try:
    import google.colab
    print("✅ Running in Google Colab!")
    
    # GPU check
    try:
        import torch
        print(f"GPU available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
    except:
        print("PyTorch not available")
        
except ImportError:
    print("❌ Not in Colab environment")

print("✅ Drive-based execution successful!")
'''
        
        # Upload script
        from googleapiclient.http import MediaIoBaseUpload
        import io
        
        media = MediaIoBaseUpload(
            io.BytesIO(script_content.encode('utf-8')),
            mimetype='text/plain'
        )
        
        file_metadata = {
            'name': 'automated_execution_test.py',
            'parents': ['1ruRdOXUJi16sHgDtpgxqtR7A7g7J8PpA']
        }
        
        result = drive_service.files().create(
            body=file_metadata,
            media_body=media
        ).execute()
        
        print(f"✅ Drive execution script uploaded: {result['id']}")
        return True
        
    except Exception as e:
        print(f"❌ Drive execution test failed: {e}")
        return False

def test_direct_colab_connection():
    """Test connecting directly to a running Colab instance"""
    
    print("\n🧪 Testing Direct Colab Connection")
    print("-" * 35)
    
    try:
        # Test if we can connect to existing Colab notebooks
        notebook_ids = [
            '1_qN_bOe4dlG9URQ634Rdf6ihQRqNrI5k',  # Previous notebook
            '1tWRrTlG_rBLdUb9Vs16i9DURsJiluN_Z'   # Working automation notebook
        ]
        
        for notebook_id in notebook_ids:
            test_notebook_connection(notebook_id)
            
    except Exception as e:
        print(f"❌ Direct connection test failed: {e}")

def test_notebook_connection(notebook_id):
    """Test connecting to a specific notebook"""
    
    print(f"🔍 Testing notebook: {notebook_id}")
    
    try:
        # Try different connection methods
        base_url = f"https://colab.research.google.com/drive/{notebook_id}"
        
        # Test various endpoints
        endpoints = [
            f"{base_url}/api/kernels",
            f"https://colab.research.google.com/api/kernels/{notebook_id}",
            f"https://colab.research.google.com/api/sessions/{notebook_id}"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, timeout=5)
                print(f"   {endpoint}: {response.status_code}")
            except:
                print(f"   {endpoint}: Connection failed")
                
    except Exception as e:
        print(f"❌ Notebook connection failed: {e}")

if __name__ == "__main__":
    test_colab_execution_api()
    test_direct_colab_connection()
    
    print("\n" + "=" * 50)
    print("🎯 API INVESTIGATION RESULTS")
    print("=" * 50)
    print("Let me analyze what's possible with service account...")
    
    print("\n💡 Next steps:")
    print("1. Investigate Google Colab's internal APIs")
    print("2. Test VM-based Jupyter alternatives") 
    print("3. Explore Cloud Run with Jupyter")
    print("4. Check if Colab supports service account execution")