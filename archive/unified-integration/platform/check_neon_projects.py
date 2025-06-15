#!/usr/bin/env python3
"""
Check and manage Neon projects.
"""

import requests
import json

NEON_API_KEY = "napi_s8buji2qmt4ht1zg1a7rw9je2er18bkale1w0glskg7918l6cmynnjvu1cb8iyh5"
NEON_API_URL = "https://console.neon.tech/api/v2"

headers = {
    "Authorization": f"Bearer {NEON_API_KEY}",
    "Content-Type": "application/json"
}

def check_projects():
    """List all projects."""
    
    print("🔍 Checking Neon projects...\n")
    
    response = requests.get(f"{NEON_API_URL}/projects", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        projects = data.get('projects', [])
        
        print(f"Found {len(projects)} project(s):\n")
        
        for project in projects:
            print(f"📁 Project: {project.get('name', 'unnamed')}")
            print(f"   ID: {project.get('id')}")
            print(f"   Created: {project.get('created_at', 'unknown')}")
            print(f"   Region: {project.get('region_id', 'unknown')}")
            
            # Try to get connection string from project data
            if 'connection_uris' in project:
                for uri in project['connection_uris']:
                    print(f"   Connection: {uri.get('connection_uri', 'not available')}")
            
            print()
        
        return projects
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return []

def get_project_details(project_id):
    """Get detailed info for a specific project."""
    
    print(f"\n🔍 Getting details for project: {project_id}\n")
    
    # Get project info
    response = requests.get(f"{NEON_API_URL}/projects/{project_id}", headers=headers)
    
    if response.status_code == 200:
        project = response.json()
        print("Project details:")
        print(json.dumps(project, indent=2))
        
        # Try to get connection string from operations
        ops_response = requests.get(
            f"{NEON_API_URL}/projects/{project_id}/operations",
            headers=headers
        )
        
        if ops_response.status_code == 200:
            operations = ops_response.json()
            for op in operations.get('operations', []):
                if op.get('action') == 'create_project' and op.get('status') == 'finished':
                    if 'project' in op:
                        print("\n📊 From operations:")
                        print(json.dumps(op['project'], indent=2))

if __name__ == "__main__":
    projects = check_projects()
    
    if projects:
        # Get details for the first project
        project_id = projects[0]['id']
        get_project_details(project_id)