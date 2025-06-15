#!/usr/bin/env python3
"""Clear user blocks - emergency utility"""

import os
import json
from datetime import datetime

# Find and clear blocks
block_files = [
    'user_profiles.json',
    'blocked_users.json',
    '.blocked_users.json',
    'data/user_profiles.json'
]

for file_path in block_files:
    if os.path.exists(file_path):
        print(f"Found {file_path}")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Clear blocks
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict):
                        if 'blocked_until' in data[key]:
                            data[key]['blocked_until'] = None
                        if 'status' in data[key]:
                            data[key]['status'] = 'active'
                        if 'permanent_block' in data[key]:
                            data[key]['permanent_block'] = False
            
            # Save cleaned data
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Cleared blocks in {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# Also try to clear in-memory blocks by restarting
print("\nTo fully clear blocks, restart the Flask app:")
print("1. Press Ctrl+C in the terminal running the app")
print("2. Run: python3 app.py")
print("\nOr simply refresh your browser and try again - blocks may be cleared.")