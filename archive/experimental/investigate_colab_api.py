#!/usr/bin/env python3
"""
Deep investigation of Colab APIs that might work with service account
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

def investigate_working_endpoints():
    """Investigate the endpoints that returned 200"""
    
    print("🔍 INVESTIGATING WORKING COLAB ENDPOINTS")
    print("=" * 50)
    
    # The endpoints that returned 200
    working_endpoints = [
        'https://colab.research.google.com/drive/1_qN_bOe4dlG9URQ634Rdf6ihQRqNrI5k/api/kernels',
        'https://colab.research.google.com/drive/1tWRrTlG_rBLdUb9Vs16i9DURsJiluN_Z/api/kernels'
    ]
    
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests
        
        # Load service account
        creds_path = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
        
        with open(creds_path) as f:
            sa_info = json.load(f)
        
        credentials = service_account.Credentials.from_service_account_info(
            sa_info, scopes=[
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/colab',
                'https://www.googleapis.com/auth/cloud-platform'
            ]
        )
        
        # Get access token
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        
        headers = {
            'Authorization': f'Bearer {credentials.token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible; ServiceAccount/1.0)'
        }
        
        print(f"✅ Service account token: {credentials.token[:50]}...")
        
        for endpoint in working_endpoints:
            print(f"\n🔍 Investigating: {endpoint}")
            investigate_endpoint(endpoint, headers)
            
    except Exception as e:
        print(f"❌ Setup error: {e}")

def investigate_endpoint(endpoint, headers):
    """Deep dive into a specific endpoint"""
    
    try:
        # GET request to see what's available
        print("📥 GET request...")
        response = requests.get(endpoint, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON Response: {json.dumps(data, indent=2)}")
                
                # If we got kernels, try to interact with them
                if isinstance(data, list) and len(data) > 0:
                    test_kernel_interaction(endpoint, headers, data)
                    
            except:
                print(f"   📄 Text Response: {response.text[:200]}")
        else:
            print(f"   ❌ Error: {response.text[:200]}")
            
        # Try POST to create/execute
        test_execution_methods(endpoint, headers)
        
    except Exception as e:
        print(f"❌ Endpoint investigation failed: {e}")

def test_kernel_interaction(endpoint, headers, kernels):
    """Test interacting with discovered kernels"""
    
    print(f"\n🧪 Testing kernel interaction...")
    
    try:
        if kernels and len(kernels) > 0:
            kernel = kernels[0]
            kernel_id = kernel.get('id')
            
            if kernel_id:
                print(f"   🎯 Found kernel: {kernel_id}")
                
                # Try to execute code in this kernel
                execute_endpoint = f"{endpoint}/{kernel_id}/execute"
                
                execute_payload = {
                    'code': 'print("🔥 SERVICE ACCOUNT EXECUTION TEST")\nprint("✅ This is running via service account!")',
                    'silent': False
                }
                
                print(f"   📤 Sending execution request...")
                exec_response = requests.post(
                    execute_endpoint, 
                    headers=headers, 
                    json=execute_payload,
                    timeout=30
                )
                
                print(f"   Execution status: {exec_response.status_code}")
                print(f"   Execution response: {exec_response.text[:300]}")
                
                if exec_response.status_code == 200:
                    print("   🎉 EXECUTION SUCCESSFUL!")
                    return True
                    
    except Exception as e:
        print(f"   ❌ Kernel interaction failed: {e}")
    
    return False

def test_execution_methods(endpoint, headers):
    """Test different execution methods"""
    
    print(f"\n🧪 Testing execution methods...")
    
    methods_to_test = [
        {
            'method': 'POST',
            'path': '',
            'payload': {
                'code': 'print("Hello from service account!")',
                'type': 'execute_request'
            }
        },
        {
            'method': 'POST', 
            'path': '/execute',
            'payload': {
                'code': 'print("Service account execution test")'
            }
        },
        {
            'method': 'POST',
            'path': '/kernel',
            'payload': {
                'name': 'python3'
            }
        }
    ]
    
    for method_test in methods_to_test:
        try:
            test_endpoint = endpoint + method_test['path']
            print(f"   🔍 {method_test['method']} {test_endpoint}")
            
            if method_test['method'] == 'POST':
                response = requests.post(
                    test_endpoint,
                    headers=headers,
                    json=method_test['payload'],
                    timeout=15
                )
            else:
                response = requests.get(test_endpoint, headers=headers, timeout=15)
            
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"      ✅ SUCCESS: {response.text[:200]}")
            elif response.status_code in [201, 202]:
                print(f"      ✅ ACCEPTED: {response.text[:200]}")
            else:
                print(f"      ❌ Failed: {response.text[:100]}")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")

def test_alternative_apis():
    """Test alternative Google APIs that might work"""
    
    print("\n🔬 TESTING ALTERNATIVE GOOGLE APIS")
    print("-" * 45)
    
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # Load service account
        creds_path = '/home/sundeepg8/projects/colab-bridge/credentials/automation-engine-463103-ee5a06e18248.json'
        
        with open(creds_path) as f:
            sa_info = json.load(f)
        
        credentials = service_account.Credentials.from_service_account_info(
            sa_info, scopes=[
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/compute',
                'https://www.googleapis.com/auth/notebooks'
            ]
        )
        
        print("✅ Service account loaded for alternative APIs")
        
        # Test Notebooks API
        try:
            notebooks_service = build('notebooks', 'v1', credentials=credentials)
            
            project_id = 'automation-engine-463103'
            
            # List existing instances
            locations = ['us-central1-a', 'us-west1-a', 'us-east1-a']
            
            for location in locations:
                try:
                    instances = notebooks_service.projects().locations().instances().list(
                        parent=f'projects/{project_id}/locations/{location}'
                    ).execute()
                    
                    print(f"✅ Notebooks API working for {location}")
                    print(f"   Instances: {len(instances.get('instances', []))}")
                    
                    # Try to create a managed notebook
                    if test_create_managed_notebook(notebooks_service, project_id, location):
                        return True
                    
                except Exception as e:
                    print(f"❌ {location}: {e}")
                    
        except Exception as e:
            print(f"❌ Notebooks API failed: {e}")
        
        # Test Compute API for custom VM
        test_compute_jupyter_vm(credentials)
        
    except Exception as e:
        print(f"❌ Alternative APIs test failed: {e}")

def test_create_managed_notebook(notebooks_service, project_id, location):
    """Test creating a managed Jupyter notebook"""
    
    print(f"🚀 Attempting to create managed notebook in {location}...")
    
    try:
        instance_config = {
            'machineType': f'projects/{project_id}/zones/{location}/machineTypes/e2-standard-2',
            'vmImage': {
                'project': 'deeplearning-platform-release',
                'imageFamily': 'tf-latest-cpu'
            },
            'metadata': {
                'startup-script': '''#!/bin/bash
echo "Starting automated Jupyter..."
pip install -q google-auth google-api-python-client
jupyter lab --ip=0.0.0.0 --port=8080 --no-browser --allow-root &
'''
            }
        }
        
        operation = notebooks_service.projects().locations().instances().create(
            parent=f'projects/{project_id}/locations/{location}',
            instanceId='automated-jupyter',
            body=instance_config
        ).execute()
        
        print(f"✅ Managed notebook creation started: {operation['name']}")
        
        # Wait for completion
        wait_for_operation(notebooks_service, operation)
        
        return True
        
    except Exception as e:
        print(f"❌ Managed notebook creation failed: {e}")
        return False

def wait_for_operation(service, operation):
    """Wait for long-running operation to complete"""
    
    print("⏳ Waiting for operation to complete...")
    
    try:
        operation_name = operation['name']
        
        for i in range(30):  # Wait up to 5 minutes
            op_result = service.projects().locations().operations().get(
                name=operation_name
            ).execute()
            
            if op_result.get('done'):
                if 'error' in op_result:
                    print(f"❌ Operation failed: {op_result['error']}")
                else:
                    print(f"✅ Operation completed successfully!")
                return op_result
            
            print(f"   Still creating... ({i+1}/30)")
            time.sleep(10)
        
        print("⏰ Operation timed out")
        return None
        
    except Exception as e:
        print(f"❌ Operation monitoring failed: {e}")
        return None

def test_compute_jupyter_vm(credentials):
    """Test creating a Compute Engine VM with Jupyter"""
    
    print("\n🚀 Testing Compute Engine VM with Jupyter...")
    
    try:
        from googleapiclient.discovery import build
        
        compute_service = build('compute', 'v1', credentials=credentials)
        project_id = 'automation-engine-463103'
        zone = 'us-central1-a'
        
        vm_config = {
            'name': 'jupyter-automation-vm',
            'machineType': f'projects/{project_id}/zones/{zone}/machineTypes/e2-standard-2',
            'disks': [{
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': 'projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts'
                }
            }],
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [{'type': 'ONE_TO_ONE_NAT'}]
            }],
            'metadata': {
                'items': [{
                    'key': 'startup-script',
                    'value': '''#!/bin/bash
apt-get update
apt-get install -y python3-pip
pip3 install jupyter google-auth google-api-python-client

# Create automated execution script
cat > /home/automated_executor.py << 'EOF'
#!/usr/bin/env python3
"""
Automated code executor running on VM
"""
import os
import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

print("🚀 Automated executor starting on VM...")

# Execute code requests continuously
while True:
    try:
        # Check for requests and execute them
        print("⏳ Checking for requests...")
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(30)
EOF

python3 /home/automated_executor.py &

# Start Jupyter for manual access
jupyter lab --ip=0.0.0.0 --port=8080 --no-browser --allow-root &
'''
                }]
            }
        }
        
        operation = compute_service.instances().insert(
            project=project_id,
            zone=zone,
            body=vm_config
        ).execute()
        
        print(f"✅ VM creation started: {operation}")
        return True
        
    except Exception as e:
        print(f"❌ VM creation failed: {e}")
        return False

if __name__ == "__main__":
    investigate_working_endpoints()
    test_alternative_apis()
    
    print("\n" + "=" * 50)
    print("🎯 INVESTIGATION SUMMARY")
    print("=" * 50)
    print("📋 What we discovered:")
    print("   • Some Colab endpoints return 200 with service account")
    print("   • Need to test kernel interaction methods")
    print("   • Alternative: Create managed Jupyter instances")
    print("   • Alternative: Custom VM with Jupyter automation")
    print("\n💡 Next: Test the most promising approaches...")