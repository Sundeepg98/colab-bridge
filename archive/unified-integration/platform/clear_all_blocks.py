#!/usr/bin/env python3
"""Clear all user blocks in user_profiles directory"""

import os
import json
import glob

profile_dir = "/var/projects/ai-integration-platform/user_profiles"
files = glob.glob(f"{profile_dir}/*.json")

cleared = 0
for file_path in files:
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        modified = False
        
        # Clear blocked_until
        if isinstance(data, dict) and 'blocked_until' in data:
            data['blocked_until'] = None
            modified = True
            
        # Clear status if blocked
        if isinstance(data, dict) and data.get('status') == 'blocked':
            data['status'] = 'active'
            modified = True
            
        # Clear permanent_block
        if isinstance(data, dict) and 'permanent_block' in data:
            data['permanent_block'] = False
            modified = True
        
        if modified:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            cleared += 1
            print(f"Cleared block in: {os.path.basename(file_path)}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

print(f"\nCleared {cleared} blocked user profiles")
print("All users should now be unblocked!")